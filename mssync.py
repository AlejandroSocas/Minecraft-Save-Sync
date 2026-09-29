import argparse
from pathlib import Path
import json
import shutil
import sys
import psutil
import pystray
from PIL import Image, ImageDraw
import threading
import time

DIRECTORIO_SCRIPT = Path(__file__).parent
ARCHIVO_CONFIG = DIRECTORIO_SCRIPT / "config.json"

# Variable global para el idioma por defecto
idioma_actual = "en"

# Diccionario global de traducciones
TEXTOS = {
  "en": {
    "config_not_found": "Configuration file not found",
    "config_incomplete": "Error: Incomplete configuration file. Configure both paths first.",
    "path_not_exist": "The path {} does not exist",
    "desc": "Minecraft world synchronizer",
    "help_sync": "Synchronizes local and cloud worlds",
    "help_slp": "Sets the local path for the worlds",
    "help_scp": "Sets the cloud path for the worlds",
    "help_dr": "Performs a simulation of the synchronization without modifying files",
    "help_bla": "Adds one or more worlds to the blacklist",
    "help_blr": "Removes one or more worlds from the blacklist",
    "help_lang": "Sets the language (en/es)",
    "help_tray": "Starts the program in the system tray",
    "help_delay": "Delays the start by 5 minutes",
    "help_interval": "Minutes between each automatic synchronization",
    "bl_already": "The world '{}' was already in the blacklist",
    "bl_added": "Added world '{}' to the blacklist",
    "bl_removed": "Removed world '{}' from the blacklist",
    "bl_not_in": "The world '{}' was not in the blacklist",
    "bl_empty": "The blacklist is empty",
    "sync_init": "Starting synchronization...",
    "sync_dry": "Starting simulation (dry run)",
    "sync_abort": "Synchronization aborted",
    "upload_new": "Uploading new world to the cloud: {}",
    "upload_dry": "Copied world [{}] to the cloud [{}]",
    "download_new": "Downloading new world to local: {}",
    "download_dry": "Copied from cloud [{}] to local directory [{}]",
    "overwrite_cloud": "Overwriting the cloud with the local version of {}...",
    "overwrite_cloud_dry": "Overwrote the cloud world [{}] with the local version of [{}]",
    "overwrite_local": "Overwriting local with the cloud version of {}...",
    "overwrite_local_dry": "Overwrote the local world [{}] with the cloud version of [{}]",
    "synced_already": "The world {} is already synchronized",
    "synced_dry": "Nothing happened because both versions of world '{}' were correctly synchronized",
    "corrupt_warning": "Warning: The world {} seems to be corrupted or is missing level.dat",
    "saving_local": "Saving new local path: {}",
    "saving_cloud": "Saving new cloud path: {}",
    "saving_lang": "Language set to: {}",
    "critic_error": "Critical error during copying {}: {}",
    "world_copied": "World '{}' successfully copied.",
    "tray_sync": "Synchronize now",
    "tray_auto": "Autostart",
    "tray_exit": "Exit",
    "tray_title": "Minecraft Sync",
    "sync_in_progress": "A synchronization is already in progress, skipping...",
    "mc_running": "Cannot synchronize: Minecraft is currently running."
  },
  "es": {
    "config_not_found": "No se ha encontrado el archivo de configuración",
    "config_incomplete": "Error: El archivo de configuración está incompleto. Configura ambas rutas primero.",
    "path_not_exist": "La ruta {} no existe",
    "desc": "Sincronizador de mundos de Minecraft",
    "help_sync": "Sincroniza los mundos locales y en la nube",
    "help_slp": "Establece la ruta local de los mundos",
    "help_scp": "Establece la ruta de la nube de los mundos",
    "help_dr": "Realiza una simulación de la sincronización sin modificar archivos",
    "help_bla": "Agrega uno o más mundos a la lista negra",
    "help_blr": "Elimina uno o más mundos de la lista negra",
    "help_lang": "Establece el idioma (en/es)",
    "help_tray": "Inicia el programa en la bandeja del sistema",
    "help_delay": "Retrasa el inicio 5 minutos",
    "help_interval": "Minutos entre cada sincronización automática",
    "bl_already": "El mundo '{}' ya estaba en la blacklist",
    "bl_added": "Se ha añadido el mundo '{}' a la lista negra",
    "bl_removed": "Se ha quitado el mundo '{}' de la lista negra",
    "bl_not_in": "El mundo '{}' no estaba en la lista negra",
    "bl_empty": "La blacklist está vacía",
    "sync_init": "Iniciando sincronización...",
    "sync_dry": "Iniciando simulación (dry run)",
    "sync_abort": "Sincronización abortada",
    "upload_new": "Subiendo mundo nuevo a la nube: {}",
    "upload_dry": "Se ha copiado el mundo [{}] en la nube [{}]",
    "download_new": "Descargando mundo nuevo a local: {}",
    "download_dry": "Se ha copiado de la nube [{}] al directorio local [{}]",
    "overwrite_cloud": "Sobrescribiendo la nube con la versión local de {}...",
    "overwrite_cloud_dry": "Se ha sobreescrito el mundo en la nube [{}] con la versión local de [{}]",
    "overwrite_local": "Sobrescribiendo local con la versión de la nube de {}...",
    "overwrite_local_dry": "Se ha sobreescrito el mundo en local [{}] con la versión en la nube [{}]",
    "synced_already": "El mundo {} se encuentra ya sincronizado",
    "synced_dry": "No ha ocurrido nada porque las dos versiones del mundo '{}' estaban correctamente sincronizadas",
    "corrupt_warning": "Aviso: El mundo {} parece estar corrupto o no tiene level.dat",
    "saving_local": "Guardando nueva ruta local: {}",
    "saving_cloud": "Guardando nueva ruta de la nube: {}",
    "saving_lang": "Idioma establecido a: {}",
    "critic_error": "Error crítico durante la copia de {}: {}",
    "world_copied": "Mundo '{}' copiado con éxito.",
    "tray_sync": "Sincronizar ahora",
    "tray_auto": "Autoarranque",
    "tray_exit": "Salir",
    "tray_title": "Minecraft Sync",
    "sync_in_progress": "Ya hay una sincronización en curso, omitiendo...",
    "mc_running": "No se puede sincronizar: Minecraft se encuentra en ejecución."
  }
}


def t(clave):
  """Función que devuelve el texto traducido"""
  return TEXTOS.get(idioma_actual, TEXTOS["en"]).get(clave, clave)


def pre_cargar_idioma():
  """Carga el idioma antes de configurar argparse para traducir el menú de ayuda"""
  global idioma_actual
  if ARCHIVO_CONFIG.exists():
    try:
      with open(ARCHIVO_CONFIG, "r") as archivo:
        datos = json.load(archivo)
        if "idioma" in datos:
          idioma_actual = datos["idioma"]
    except json.JSONDecodeError:
      pass


def cargar_configuracion():
  """Carga la configuración del programa desde el archivo config.json"""
  try:
    with open(ARCHIVO_CONFIG, "r") as archivo:
      datos = json.load(archivo)
  except FileNotFoundError:
    print(t("config_not_found"))
    return None
  
  if "ruta_local" not in datos or "ruta_nube" not in datos:
    print(t("config_incomplete"))
    return None

  config = {
    "ruta_local": Path(datos["ruta_local"]),
    "ruta_nube": Path(datos["ruta_nube"]),
    "blacklist": [],
    "estado_sync": {}
  }

  if "blacklist" in datos:
    config["blacklist"] = datos["blacklist"]
  if "estado_sync" in datos:
    config["estado_sync"] = datos["estado_sync"]

  return config

# Comprueba si una ruta pasada existe o no
def existe_ruta(ruta):
  if not ruta.exists():
    print(t("path_not_exist").format(ruta))
    return False
  else:
    return True


def minecraft_en_ejecucion():
  """Comprueba si minecraft se encuentra en ejecución"""
  for proc in psutil.process_iter(['name', 'cmdline']):
    try:
      nombre = proc.info['name'].lower()
      cmdline = proc.info.get('cmdline')
      cmdline_str = " ".join(cmdline).lower() if cmdline else ""
      
      # Detecta la máquina virtual de Java corriendo Minecraft o versiones nativas
      if ('java' in nombre and 'minecraft' in cmdline_str) or 'minecraft' in nombre:
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
      pass
  return False


def _ejecutar_sincronizacion_interna(args):
  """Ejecuta la lógica de sincronización utilizando archivos ZIP para subirlo a la nube"""
  guardar_json = False

  # Sincronización iniciada
  if not args.dry_run:
    print(t("sync_init"))
  else:
    print(t("sync_dry"))

  # Cargamos las rutas desde el archivo config.json
  rutas = cargar_configuracion()

  # Si no hay rutas configuradas salimos del programa
  if not rutas:
    print(t("sync_abort"))
    sys.exit(1)
  if not existe_ruta(rutas["ruta_local"]) or not existe_ruta(rutas["ruta_nube"]):
    print(t("sync_abort"))
    sys.exit(2)

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
      print(t("upload_new").format(mundo))
      ruta_mundo_local = rutas["ruta_local"] / mundo
      ruta_mundo_nube_base = rutas["ruta_nube"] / mundo 
      ruta_mundo_nube_zip = rutas["ruta_nube"] / f"{mundo}.zip"
      
      try:
        if not args.dry_run: 
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
          
          print(t("world_copied").format(mundo))
        else:
          print(t("upload_dry").format(ruta_mundo_local, ruta_mundo_nube_zip))
      except Exception as e:
        print(t("critic_error").format(mundo, e))
        continue
  
  # Descargar mundos nuevos de la nube
  for mundo in mundos_nube[:]:
    if mundo in rutas["blacklist"]:
      continue
    if not mundo in mundos_locales:
      mundos_nube.remove(mundo)
      print(t("download_new").format(mundo))
      ruta_mundo_local = rutas["ruta_local"] / mundo
      ruta_mundo_nube_zip = rutas["ruta_nube"] / f"{mundo}.zip"
      
      try:
        if not args.dry_run:
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
          
          print(t("world_copied").format(mundo))
        else:
          print(t("download_dry").format(ruta_mundo_nube_zip, ruta_mundo_local))
      except Exception as e:
        print(t("critic_error").format(mundo, e))
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
          if not args.dry_run:
            print(t("overwrite_cloud").format(mundo))
            shutil.make_archive(str(ruta_mundo_nube_base), 'zip', str(ruta_mundo_local))
            
            if "estado_sync" not in datos: datos["estado_sync"] = {}
            datos["estado_sync"][mundo] = {
              "local": tiempo_modificado_local,
              "nube": int(ruta_mundo_nube_zip.stat().st_mtime) 
            }
            guardar_json = True
            
            print(t("world_copied").format(mundo))
          else:
            print(t("overwrite_cloud_dry").format(ruta_mundo_nube_zip, ruta_mundo_local))
        except Exception as e:
          print(t("critic_error").format(mundo, e))
          continue
      
      elif nube_ha_cambiado and not local_ha_cambiado:
        try:
          if not args.dry_run:
            print(t("overwrite_local").format(mundo))
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
            
            print(t("world_copied").format(mundo))
          else:
            print(t("overwrite_local_dry").format(ruta_mundo_local, ruta_mundo_nube_zip))
        except Exception as e:
          print(t("critic_error").format(mundo, e))
          continue
      
      else:
        if not args.dry_run:
          print(t("synced_already").format(mundo))
        else:
          print(t("synced_dry").format(mundo))
    else:
      print(t("corrupt_warning").format(mundo))

  if guardar_json:
    with open(ARCHIVO_CONFIG, "w") as archivo:
      json.dump(datos, archivo, indent=2)


sync_lock = threading.Lock()


def ejecutar_sincronizacion(args):
  """Lanza la lógica de sincronización protegiendo contra ejecuciones concurrentes"""
  if not sync_lock.acquire(blocking=False):
    print(t("sync_in_progress"))
    return
  try:
    _ejecutar_sincronizacion_interna(args)
  finally:
    sync_lock.release()


def tarea_en_segundo_plano(intervalo_minutos, args, icono):
  # Retraso inicial para dar tiempo a dibujar el icono
  time.sleep(2)
  
  # Si el usuario activó el delay (-d), esperamos 300 segundos adicionales (5 minutos)
  if args.delay:
    for _ in range(300):
      # Si el usuario le da a "Salir" durante estos 5 minutos, abortamos limpiamente
      if not icono.visible:
        return
      time.sleep(1)
  
  # Hacemos la primera copia tras el arranque (y el posible delay)
  if not minecraft_en_ejecucion():
    ejecutar_sincronizacion(args)

  # Iniciamos el bucle del temporizador normal
  segundos_espera = intervalo_minutos * 60
  while icono.visible:
    for _ in range(segundos_espera):
      if not icono.visible:
        return
      time.sleep(1)
      
    if not minecraft_en_ejecucion():
      ejecutar_sincronizacion(args)


def accion_sincronizar(args):
  """Lanza la lógica de sincronización si minecraft no está en ejecución"""
  if minecraft_en_ejecucion():
    print(t("mc_running"))
    return
  threading.Thread(target=ejecutar_sincronizacion, args=(args,), daemon=True).start()


def accion_salir(icono, item):
  """Cierra el programa"""
  icono.stop()


def iniciar_tray(intervalo_minutos, args):
  """Inicia el tray según los argumentos pasados"""
  imagen = crear_icono()

  # Crea el menú contextual al pulsar el icono de del tray
  menu = pystray.Menu(
    pystray.MenuItem(t("tray_sync"), lambda icono, item: accion_sincronizar(args)),
    pystray.MenuItem(t("tray_auto"), alternar_autoarranque, checked=lambda item: autoarranque_activado()),
    pystray.MenuItem(t("tray_exit"), accion_salir)
  )
  
  icono = pystray.Icon("mssync", imagen, t("tray_title"), menu)

  # Lanza en segundo plano la lógica del programa
  hilo = threading.Thread(
    target=tarea_en_segundo_plano, 
    args=(intervalo_minutos, args, icono), 
    daemon=True
  )
  hilo.start()
  
  icono.run()


def crear_icono():
  """Crea un icono básico para el tray"""
  imagen = Image.new('RGB', (64, 64), color=(73, 109, 137))
  dibujo = ImageDraw.Draw(imagen)
  dibujo.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
  return imagen


def obtener_ruta_autoarranque():
  """Obtiene la ruta del fichero de autoarranque dependiendo del SO"""
  if sys.platform.startswith('linux'):
    return Path.home() / ".config" / "autostart" / "mssync.desktop"
  elif sys.platform == "win32":
    return Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "mssync.bat"
  return None


def autoarranque_activado():
  """Comprueba si el autoarranque ya está activado"""
  ruta = obtener_ruta_autoarranque()
  return ruta.exists() if ruta else False


def alternar_autoarranque(icono, item):
  """Activa/desactiva el autoarranque del programa al iniciar el SO"""
  ruta = obtener_ruta_autoarranque()
  if not ruta:
    return

  # Si no está activado lo activamos
  if ruta.exists():
    ruta.unlink()
  else:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    
    if getattr(sys, 'frozen', False):
      comando = f'"{sys.executable}" --tray --delay'
    else:
      comando = f'"{sys.executable}" "{Path(__file__).resolve()}" --tray --delay'
    
    if sys.platform.startswith('linux'):
      contenido = f"[Desktop Entry]\nType=Application\nExec={comando}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName=Minecraft Sync Tray\n"
      ruta.write_text(contenido)
    elif sys.platform == "win32":
      ruta.write_text(f'@echo off\nstart "" /b {comando}\n')


def main():
  global idioma_actual

  # Cargamos el idioma configurado
  pre_cargar_idioma()

  # Recibimos los argumentos de la línea de comandos y los añadimos a args
  parser = argparse.ArgumentParser(description=t("desc"))
  parser.add_argument("comando", choices=["sync"], nargs="?", help=t("help_sync"))
  parser.add_argument("-slp", "--setlocalp", help=t("help_slp"))
  parser.add_argument("-scp", "--setcloudp", help=t("help_scp"))
  parser.add_argument("-dr", "--dry-run", action="store_true", help=t("help_dr"))
  parser.add_argument("-bla", "--blacklist-add", nargs='+', help=t("help_bla"))
  parser.add_argument("-blr", "--blacklist-remove", nargs='+', help=t("help_blr"))
  parser.add_argument("-l", "--lang", choices=["en", "es"], help=t("help_lang"))
  parser.add_argument("-t", "--tray", action="store_true", help=t("help_tray"))
  parser.add_argument("-d", "--delay", action="store_true", help=t("help_delay"))
  parser.add_argument("-i", "--interval", type=int, default=30, help=t("help_interval"))
  
  args = parser.parse_args()

  # Leemos la configuración para procesar argumentos de configuración antes de sincronizar
  datos = {}
  if ARCHIVO_CONFIG.exists():
    with open(ARCHIVO_CONFIG, "r") as archivo:
      datos = json.load(archivo)
  
  guardar_json_main = False

  # Cambiamos el idioma
  if args.lang:
    idioma_actual = args.lang
    datos["idioma"] = args.lang
    print(t("saving_lang").format(args.lang))
    guardar_json_main = True

  # Añadimos mundos a la blacklist
  if args.blacklist_add:
    for mundo in args.blacklist_add:
      if not "blacklist" in datos:
        datos["blacklist"] = []
      if mundo in datos["blacklist"]:
        print(t("bl_already").format(mundo))
      else:
        datos["blacklist"].append(mundo)
        print(t("bl_added").format(mundo))
        guardar_json_main = True

  # Eliminamos mundos de la blacklist
  if args.blacklist_remove:
    if "blacklist" in datos and datos["blacklist"]:
      for mundo in args.blacklist_remove:
        if mundo in datos["blacklist"]:
          datos["blacklist"].remove(mundo)
          print(t("bl_removed").format(mundo))
        else:
          print(t("bl_not_in").format(mundo))
        guardar_json_main = True
    else:
      print(t("bl_empty"))

  # Establecemos la ruta local de los mundos
  if args.setlocalp:
    print(t("saving_local").format(args.setlocalp))
    datos["ruta_local"] = args.setlocalp
    guardar_json_main = True

  # Establecemos la ruta de la nube de los mundos
  if args.setcloudp:
    print(t("saving_cloud").format(args.setcloudp))
    datos["ruta_nube"] = args.setcloudp
    guardar_json_main = True
  
  # Guardamos la configuración antes de iniciar el tray/sync
  if guardar_json_main:
    with open(ARCHIVO_CONFIG, "w") as archivo:
      json.dump(datos, archivo, indent=2)
  
  # Arranque de los motores principales
  if args.tray:
    iniciar_tray(args.interval, args)
  elif args.comando == "sync" or args.dry_run:
    ejecutar_sincronizacion(args)
  
  sys.exit(0)

if __name__ == "__main__":
  main()