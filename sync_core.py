from PySide6.QtCore import QObject, Signal, QThread
import shutil
import json
import sys

from config import *
from utils import *

class SyncSignals(QObject):
  """Comunicador entre hilos"""
  log_message = Signal(str)
  finished = Signal(bool)

class SyncWorker(QThread):
  """Hilo trabajador de ejecuta la sincronización"""
  def __init__(self, args, parent=None):
    super().__init__(parent)
    self.args = args
    self.signals = SyncSignals()

  def run(self):
    try:
      self._ejecutar_sincronizacion_interna()
    except Exception as e:
      self.signals.log_message.emit(f"Error inesperado: {e}")
    finally:
      # Siempre emitimos finished al acabar, haya error o no
      self.signals.finished.emit(True)

  def emit_log(self, mensaje):
    """Función de conveniencia para acortar el código"""
    self.signals.log_message.emit(mensaje)

  def _ejecutar_sincronizacion_interna(self):
    """Ejecuta la lógica de sincronización utilizando archivos ZIP para subirlo a la nube"""
    guardar_json = False

    # Sincronización iniciada
    if not self.args.dry_run:
      self.emit_log(t("sync_init"))
    else:
      self.emit_log(t("sync_dry"))

    # Cargamos las rutas desde el archivo config.json
    rutas = cargar_configuracion()

    # Si no hay rutas configuradas salimos del programa
    if not rutas:
      self.emit_log(t("sync_abort"))

    # Comprobamos que las rutas existen
    if not rutas["ruta_local"].exists():
      self.emit_log(t("path_not_exist").format(rutas["ruta_local"]))
      self.emit_log(t("sync_abort"))
      return
    if not rutas["ruta_nube"].exists():
      self.emit_log(t("path_not_exist").format(rutas["ruta_nube"]))
      self.emit_log(t("sync_abort"))
      return

    # Cargamos el resto desde el archivo de configuración
    datos = {}
    if ARCHIVO_CONFIG.exists():
      with open(ARCHIVO_CONFIG, "r") as archivo:
        datos = json.load(archivo)

    # Obtenemos los mundos locales (carpetas) y los de la nube (archivos .zip)
    mundos_locales = [mundo.name for mundo in rutas["ruta_local"].iterdir() if mundo.is_dir()]
    mundos_nube = [mundo.stem for mundo in rutas["ruta_nube"].iterdir() if mundo.is_file() and mundo.suffix == '.zip']

    # Subir mundos nuevos a la nube
    for mundo in mundos_locales[:]:
      if mundo in rutas["blacklist"]:
        continue
      if not mundo in mundos_nube:
        mundos_locales.remove(mundo)
        self.signals.log_message.emit(t("upload_new").format(mundo))
        ruta_mundo_local = rutas["ruta_local"] / mundo
        ruta_mundo_nube_base = rutas["ruta_nube"] / mundo 
        ruta_mundo_nube_zip = rutas["ruta_nube"] / f"{mundo}.zip"
        
        try:
          if not self.args.dry_run: 
            # make_archive añade la extensión .zip automáticamente al final de ruta_mundo_nube_base
            shutil.make_archive(str(ruta_mundo_nube_base), 'zip', str(ruta_mundo_local))
            level_local = ruta_mundo_local / "level.dat"
            
            if level_local.exists() and ruta_mundo_nube_zip.exists():
              if "estado_sync" not in datos: 
                datos["estado_sync"] = {}
              datos["estado_sync"][mundo] = {
                "local": int(level_local.stat().st_mtime),
                "nube": int(ruta_mundo_nube_zip.stat().st_mtime)
              }
              guardar_json = True
            
            self.signals.log_message.emit(t("world_copied").format(mundo))
          else:
            self.signals.log_message.emit(t("upload_dry").format(ruta_mundo_local, ruta_mundo_nube_zip))
        except Exception as e:
          self.signals.log_message.emit(t("critic_error").format(mundo, e))
          continue
    
    # Descargar mundos nuevos de la nube
    for mundo in mundos_nube[:]:
      if mundo in rutas["blacklist"]:
        continue
      if not mundo in mundos_locales:
        mundos_nube.remove(mundo)
        self.signals.log_message.emit(t("download_new").format(mundo))
        ruta_mundo_local = rutas["ruta_local"] / mundo
        ruta_mundo_nube_zip = rutas["ruta_nube"] / f"{mundo}.zip"
        
        try:
          if not self.args.dry_run:
            # unpack_archive descomprime el contenido del zip dentro de la carpeta local
            shutil.unpack_archive(str(ruta_mundo_nube_zip), str(ruta_mundo_local))
            level_local = ruta_mundo_local / "level.dat"
            
            if level_local.exists() and ruta_mundo_nube_zip.exists():
              if "estado_sync" not in datos: 
                datos["estado_sync"] = {}
              datos["estado_sync"][mundo] = {
                "local": int(level_local.stat().st_mtime),
                "nube": int(ruta_mundo_nube_zip.stat().st_mtime)
              }
              guardar_json = True
            
            self.signals.log_message.emit(t("world_copied").format(mundo))
          else:
            self.signals.log_message.emit(t("download_dry").format(ruta_mundo_nube_zip, ruta_mundo_local))
        except Exception as e:
          self.signals.log_message.emit(t("critic_error").format(mundo, e))
          continue
    
    # Comparar fechas de los mundos existentes
    for mundo in mundos_locales:
      if mundo in rutas["blacklist"]:
        continue
      
      ruta_mundo_local = rutas["ruta_local"] / mundo
      ruta_mundo_nube_base = rutas["ruta_nube"] / mundo
      ruta_mundo_nube_zip = rutas["ruta_nube"] / f"{mundo}.zip"
      level_local = ruta_mundo_local / "level.dat"
      
      if level_local.exists() and ruta_mundo_nube_zip.exists():
        tiempo_modificado_local = int(level_local.stat().st_mtime)
        tiempo_modificado_nube = int(ruta_mundo_nube_zip.stat().st_mtime)
        
        estado_anterior = rutas["estado_sync"].get(mundo, {"local": 0, "nube": 0})
        ultimo_local_conocido = int(estado_anterior["local"])
        ultima_nube_conocida = int(estado_anterior["nube"])
        
        local_ha_cambiado = tiempo_modificado_local > ultimo_local_conocido
        nube_ha_cambiado = tiempo_modificado_nube > ultima_nube_conocida

        if local_ha_cambiado:
          try:
            if not self.args.dry_run:
              self.signals.log_message.emit(t("overwrite_cloud").format(mundo))
              shutil.make_archive(str(ruta_mundo_nube_base), 'zip', str(ruta_mundo_local))
              
              if "estado_sync" not in datos: datos["estado_sync"] = {}
              datos["estado_sync"][mundo] = {
                "local": tiempo_modificado_local,
                "nube": int(ruta_mundo_nube_zip.stat().st_mtime) 
              }
              guardar_json = True
              
              self.signals.log_message.emit(t("world_copied").format(mundo))
            else:
              self.signals.log_message.emit(t("overwrite_cloud_dry").format(ruta_mundo_nube_zip, ruta_mundo_local))
          except Exception as e:
            self.signals.log_message.emit(t("critic_error").format(mundo, e))
            continue
        
        elif nube_ha_cambiado and not local_ha_cambiado:
          try:
            if not self.args.dry_run:
              self.signals.log_message.emit(t("overwrite_local").format(mundo))
              if ruta_mundo_local.exists():
                shutil.rmtree(ruta_mundo_local)
                
              shutil.unpack_archive(str(ruta_mundo_nube_zip), str(ruta_mundo_local))
              level_local_nuevo = ruta_mundo_local / "level.dat"
              
              if "estado_sync" not in datos: datos["estado_sync"] = {}
              datos["estado_sync"][mundo] = {
                "local": int(level_local_nuevo.stat().st_mtime),
                "nube": tiempo_modificado_nube
              }
              guardar_json = True
              
              self.signals.log_message.emit(t("world_copied").format(mundo))
            else:
              self.signals.log_message.emit(t("overwrite_local_dry").format(ruta_mundo_local, ruta_mundo_nube_zip))
          except Exception as e:
            self.signals.log_message.emit(t("critic_error").format(mundo, e))
            continue
        
        else:
          if not self.args.dry_run:
            self.signals.log_message.emit(t("synced_already").format(mundo))
          else:
            self.signals.log_message.emit(t("synced_dry").format(mundo))
      else:
        self.signals.log_message.emit(t("corrupt_warning").format(mundo))

    if guardar_json:
      with open(ARCHIVO_CONFIG, "w") as archivo:
        json.dump(datos, archivo, indent=2)