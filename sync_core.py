from PySide6.QtCore import QObject, Signal, QThread
import shutil
import time

from config import *
from utils import *

# Sufijos de los elementos temporales que el programa crea en la carpeta local de mundos
SUFIJO_EXTRACCION = "__mssync_extraccion"
SUFIJO_ANTIGUO = "__mssync_antiguo"
SUFIJO_DESCARGA = "__mssync_descarga.zip"
# Marca de las copias de seguridad creadas al detectar un conflicto
MARCA_CONFLICTO = "_Conflicto_"


class MinecraftAbiertoError(Exception):
  """Se lanza cuando Minecraft se abre en mitad de una sincronización"""


def es_carpeta_interna(nombre):
  """Indica si una carpeta es temporal o una copia de conflicto (no se sincroniza)"""
  return nombre.endswith(SUFIJO_EXTRACCION) or nombre.endswith(SUFIJO_ANTIGUO) or MARCA_CONFLICTO in nombre


def borrar_ruta(ruta):
  """Borra una carpeta o un archivo si existe"""
  if ruta.is_dir():
    shutil.rmtree(ruta)
  elif ruta.exists():
    ruta.unlink()


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
      self.emit_log(t("err_unexpected").format(e))
    finally:
      # Siempre emitimos finished al acabar, haya error o no
      self.signals.finished.emit(True)

  def emit_log(self, mensaje):
    """Función de conveniencia para acortar el código"""
    self.signals.log_message.emit(mensaje)

  def _ejecutar_sincronizacion_interna(self):
    """Ejecuta la lógica de sincronización utilizando archivos ZIP para subirlo a la nube"""
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
      return

    # Comprobamos que las rutas existen
    if not rutas["ruta_local"].exists():
      self.emit_log(t("path_not_exist").format(rutas["ruta_local"]))
      self.emit_log(t("sync_abort"))
      return
    if not rutas["ruta_nube"].exists():
      self.emit_log(t("path_not_exist").format(rutas["ruta_nube"]))
      self.emit_log(t("sync_abort"))
      return

    # --- INICIO SISTEMA DE BLOQUEO (LOCK) ---
    archivo_lock = rutas["ruta_nube"] / "mssync.lock"
    
    if archivo_lock.exists():
      edad_lock = time.time() - archivo_lock.stat().st_mtime
      if edad_lock < 3600:
        self.emit_log(t("lock_active"))
        return
      else:
        self.emit_log(t("lock_obsolete"))

    try:
      archivo_lock.touch()
    except Exception as e:
      self.emit_log(t("lock_error").format(e))
      return
    # --- FIN SISTEMA DE BLOQUEO ---

    # Envolvemos el resto en try/finally para garantizar que el lock se borre al terminar
    try:
      try:
        self._sincronizar_mundos(rutas)
      except MinecraftAbiertoError:
        self.emit_log(t("mc_opened_abort"))

    finally:
      # Limpieza del archivo lock con espera
      if archivo_lock.exists():
        try:
          if not self.args.dry_run:
            self.emit_log(t("lock_wait"))
            time.sleep(30)
          archivo_lock.unlink()
        except Exception:
          pass

  def _sincronizar_mundos(self, rutas):
    """Compara los mundos locales con los de la nube y sube/descarga lo necesario"""
    ruta_local = rutas["ruta_local"]
    ruta_nube = rutas["ruta_nube"]
    blacklist = rutas["blacklist"]
    estado_sync = rutas["estado_sync"]

    # Eliminamos restos de sincronizaciones interrumpidas antes de listar los mundos
    if not self.args.dry_run:
      self._limpiar_temporales(ruta_local)

    # Obtenemos los mundos locales (carpetas) y los de la nube (archivos .zip)
    # Se excluyen las carpetas temporales y las copias de conflicto para que nunca se suban
    mundos_locales = [mundo.name for mundo in ruta_local.iterdir() if mundo.is_dir() and not es_carpeta_interna(mundo.name)]
    # Filtramos los _temp de la nube por si quedó alguno residual de versiones anteriores
    mundos_nube = [mundo.stem for mundo in ruta_nube.iterdir() if mundo.is_file() and mundo.suffix == '.zip' and not mundo.stem.endswith('_temp') and not es_carpeta_interna(mundo.stem)]

    # Subir mundos nuevos a la nube
    for mundo in mundos_locales[:]:
      if mundo in blacklist or mundo in mundos_nube:
        continue
      mundos_locales.remove(mundo)
      self.emit_log(t("upload_new").format(mundo))
      ruta_mundo_local = ruta_local / mundo
      ruta_mundo_nube_zip = ruta_nube / f"{mundo}.zip"

      try:
        if self.args.dry_run:
          self.emit_log(t("upload_dry").format(ruta_mundo_local, ruta_mundo_nube_zip))
          continue
        self._comprobar_minecraft()
        self._subir_mundo(mundo, ruta_mundo_local, ruta_nube)
        self.emit_log(t("upload_success").format(mundo))
      except MinecraftAbiertoError:
        raise
      except Exception as e:
        self.emit_log(t("critic_error").format(mundo, e))

    # Descargar mundos nuevos de la nube
    for mundo in mundos_nube[:]:
      if mundo in blacklist or mundo in mundos_locales:
        continue
      mundos_nube.remove(mundo)
      self.emit_log(t("download_new").format(mundo))
      ruta_mundo_local = ruta_local / mundo
      ruta_mundo_nube_zip = ruta_nube / f"{mundo}.zip"

      try:
        if self.args.dry_run:
          self.emit_log(t("download_dry").format(ruta_mundo_nube_zip, ruta_mundo_local))
          continue
        self._comprobar_minecraft()
        if self._descargar_mundo(mundo, ruta_mundo_nube_zip, ruta_mundo_local):
          self._guardar_estado_descarga(mundo, ruta_mundo_local, ruta_mundo_nube_zip)
          self.emit_log(t("download_success").format(mundo))
        else:
          self.emit_log(t("corrupt_cloud_skip").format(mundo))
      except MinecraftAbiertoError:
        raise
      except Exception as e:
        self.emit_log(t("critic_error").format(mundo, e))

    # Comparar fechas de los mundos existentes
    for mundo in mundos_locales:
      if mundo in blacklist:
        continue

      ruta_mundo_local = ruta_local / mundo
      ruta_mundo_nube_zip = ruta_nube / f"{mundo}.zip"
      level_local = ruta_mundo_local / "level.dat"

      if not (level_local.exists() and ruta_mundo_nube_zip.exists()):
        self.emit_log(t("corrupt_warning").format(mundo))
        continue

      tiempo_modificado_local = int(level_local.stat().st_mtime)
      tiempo_modificado_nube = int(ruta_mundo_nube_zip.stat().st_mtime)

      estado_anterior = estado_sync.get(mundo, {"local": 0, "nube": 0})
      ultimo_local_conocido = int(estado_anterior["local"])
      ultima_nube_conocida = int(estado_anterior["nube"])

      local_ha_cambiado = tiempo_modificado_local > ultimo_local_conocido
      nube_ha_cambiado = tiempo_modificado_nube > ultima_nube_conocida

      try:
        if local_ha_cambiado and nube_ha_cambiado:
          if self.args.dry_run:
            self.emit_log(t("conflict_dry").format(mundo))
            continue
          self._comprobar_minecraft()
          self.emit_log(t("conflict_both").format(mundo))
          self.emit_log(t("conflict_backup"))

          # La copia local solo se aparta cuando la versión de la nube ya está extraída y validada
          ruta_mundo_conflicto = ruta_local / f"{mundo}{MARCA_CONFLICTO}{int(time.time())}"
          if self._descargar_mundo(mundo, ruta_mundo_nube_zip, ruta_mundo_local, ruta_mundo_conflicto):
            self._guardar_estado_descarga(mundo, ruta_mundo_local, ruta_mundo_nube_zip)
            self.emit_log(t("conflict_renamed").format(ruta_mundo_conflicto.name))
          else:
            self.emit_log(t("corrupt_cloud_cancel").format(mundo))

        elif local_ha_cambiado:
          if self.args.dry_run:
            self.emit_log(t("overwrite_cloud_dry").format(ruta_mundo_nube_zip, ruta_mundo_local))
            continue
          self._comprobar_minecraft()
          self.emit_log(t("overwrite_cloud").format(mundo))
          self._subir_mundo(mundo, ruta_mundo_local, ruta_nube)
          self.emit_log(t("upload_success").format(mundo))

        elif nube_ha_cambiado:
          if self.args.dry_run:
            self.emit_log(t("overwrite_local_dry").format(ruta_mundo_local, ruta_mundo_nube_zip))
            continue
          self._comprobar_minecraft()
          self.emit_log(t("overwrite_local").format(mundo))
          if self._descargar_mundo(mundo, ruta_mundo_nube_zip, ruta_mundo_local):
            self._guardar_estado_descarga(mundo, ruta_mundo_local, ruta_mundo_nube_zip, tiempo_modificado_nube)
            self.emit_log(t("download_success").format(mundo))
          else:
            self.emit_log(t("corrupt_cloud_cancel").format(mundo))

        else:
          if not self.args.dry_run:
            self.emit_log(t("synced_already").format(mundo))
          else:
            self.emit_log(t("synced_dry").format(mundo))
      except MinecraftAbiertoError:
        raise
      except Exception as e:
        self.emit_log(t("critic_error").format(mundo, e))

  def _comprobar_minecraft(self):
    """Aborta la sincronización si Minecraft se ha abierto mientras tanto"""
    if minecraft_en_ejecucion():
      raise MinecraftAbiertoError()

  def _limpiar_temporales(self, ruta_local):
    """Elimina restos de sincronizaciones interrumpidas y restaura mundos que se quedaron apartados"""
    for elemento in list(ruta_local.iterdir()):
      nombre = elemento.name
      try:
        if elemento.is_dir() and nombre.endswith(SUFIJO_ANTIGUO):
          ruta_original = ruta_local / nombre[:-len(SUFIJO_ANTIGUO)]
          if ruta_original.exists():
            # El mundo nuevo ya está en su sitio, la copia antigua sobra
            shutil.rmtree(elemento)
            self.emit_log(t("temp_cleaned").format(nombre))
          else:
            # Se cortó justo durante el intercambio: devolvemos el mundo a su sitio
            elemento.rename(ruta_original)
            self.emit_log(t("temp_restored").format(ruta_original.name))
        elif elemento.is_dir() and nombre.endswith(SUFIJO_EXTRACCION):
          shutil.rmtree(elemento)
          self.emit_log(t("temp_cleaned").format(nombre))
        elif elemento.is_file() and nombre.endswith(SUFIJO_DESCARGA):
          elemento.unlink()
          self.emit_log(t("temp_cleaned").format(nombre))
      except Exception as e:
        self.emit_log(t("critic_error").format(nombre, e))

  def _subir_mundo(self, mundo, ruta_mundo_local, ruta_nube):
    """Comprime el mundo directamente en la nube y guarda su estado"""
    level_local = ruta_mundo_local / "level.dat"
    # Tomamos la fecha antes de comprimir para no ocultar cambios hechos durante la compresión
    tiempo_local = int(level_local.stat().st_mtime) if level_local.exists() else None

    # make_archive añade la extensión .zip automáticamente al final de la ruta base
    # Comprimimos directamente en el archivo final sin usar archivos temporales
    ruta_mundo_nube_base = ruta_nube / mundo
    shutil.make_archive(str(ruta_mundo_nube_base), 'zip', str(ruta_mundo_local))

    ruta_mundo_nube_zip = ruta_nube / f"{mundo}.zip"
    if tiempo_local is not None and ruta_mundo_nube_zip.exists():
      actualizar_estado_mundo(mundo, tiempo_local, ruta_mundo_nube_zip.stat().st_mtime)

  def _guardar_estado_descarga(self, mundo, ruta_mundo_local, ruta_mundo_nube_zip, tiempo_nube=None):
    """Guarda las fechas de un mundo recién descargado"""
    level_local = ruta_mundo_local / "level.dat"
    if level_local.exists() and ruta_mundo_nube_zip.exists():
      if tiempo_nube is None:
        tiempo_nube = ruta_mundo_nube_zip.stat().st_mtime
      actualizar_estado_mundo(mundo, level_local.stat().st_mtime, tiempo_nube)

  def _descargar_mundo(self, mundo, ruta_mundo_nube_zip, ruta_mundo_local, ruta_backup=None):
    """Descarga un mundo de la nube sin arriesgar la copia local.
    Devuelve False si el zip de la nube no es válido. Si ruta_backup se indica,
    la versión local se conserva ahí en lugar de borrarse."""
    ruta_local = ruta_mundo_local.parent
    ruta_zip_temp_local = ruta_local / f"{mundo}{SUFIJO_DESCARGA}"
    ruta_mundo_temp = ruta_local / f"{mundo}{SUFIJO_EXTRACCION}"
    ruta_mundo_antiguo = ruta_local / f"{mundo}{SUFIJO_ANTIGUO}"

    # VALIDACIÓN DE INTEGRIDAD antes de tocar nada
    if not zip_es_valido(ruta_mundo_nube_zip):
      return False

    try:
      # Partimos de cero por si quedaron restos de un intento anterior
      borrar_ruta(ruta_zip_temp_local)
      borrar_ruta(ruta_mundo_temp)

      # 1. Copiamos el zip a local (lectura secuencial rápida para rclone)
      shutil.copy2(str(ruta_mundo_nube_zip), str(ruta_zip_temp_local))

      # 2. Descomprimimos desde el disco local en una carpeta temporal
      shutil.unpack_archive(str(ruta_zip_temp_local), str(ruta_mundo_temp), 'zip')
      if not (ruta_mundo_temp / "level.dat").exists():
        raise ValueError(t("extract_no_level"))

      # Última comprobación antes de tocar el mundo local
      self._comprobar_minecraft()

      # 3. Intercambio: apartamos el mundo actual y ponemos el nuevo en su lugar
      destino_apartado = ruta_backup if ruta_backup else ruta_mundo_antiguo
      if ruta_mundo_local.exists():
        borrar_ruta(ruta_mundo_antiguo)
        ruta_mundo_local.rename(destino_apartado)
      try:
        ruta_mundo_temp.rename(ruta_mundo_local)
      except Exception:
        # Si falla, devolvemos el mundo original a su sitio
        if destino_apartado.exists() and not ruta_mundo_local.exists():
          destino_apartado.rename(ruta_mundo_local)
        raise

      # 4. Borramos la versión antigua (si falla, se limpiará en la próxima sincronización)
      shutil.rmtree(ruta_mundo_antiguo, ignore_errors=True)
      return True
    finally:
      # Los temporales se borran siempre, haya ido bien o mal
      for ruta in (ruta_zip_temp_local, ruta_mundo_temp):
        try:
          borrar_ruta(ruta)
        except Exception:
          pass
