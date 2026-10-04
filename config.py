from pathlib import Path
import json
import os
import sys
import shutil
import threading

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
    "help_block": "Blocks the autosync function",
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
    "upload_success": "The world '{}' is in the local cloud folder. Check your cloud client to see the upload progress.",
    "download_success": "The world '{}' has been successfully downloaded and copied locally.",
    "err_unexpected": "Unexpected error: {}",
    "lock_active": "Another device is currently syncing (active lock). Skipping...",
    "lock_obsolete": "Obsolete lock found. Ignoring...",
    "lock_error": "Could not create lock file: {}",
    "lock_wait": "Finishing... Waiting 30 seconds to release the lock.",
    "corrupt_cloud_skip": "Warning: Cloud file {}.zip is corrupted or incomplete. Skipping.",
    "corrupt_cloud_cancel": "Warning: Cloud file {}.zip is corrupted or incomplete. Overwrite cancelled.",
    "conflict_both": "CONFLICT! The world '{}' has been modified both locally and in the cloud.",
    "conflict_backup": "Creating local backup...",
    "conflict_renamed": "Local copy saved as '{}' (it will not be synchronized). The cloud version has been downloaded.",
    "conflict_dry": "CONFLICT (Dry Run)! The world '{}' has local and cloud changes.",
    "auto_enabled": "Autostart activated in the system.",
    "auto_disabled": "Autostart deactivated.",
    "tray_sync": "Synchronize now",
    "tray_auto": "Autostart",
    "tray_exit": "Exit",
    "tray_title": "Minecraft Sync",
    "sync_in_progress": "A synchronization is already in progress, skipping...",
    "mc_running": "Cannot synchronize: Minecraft is currently running.",
    "saving_start_parameters": "Saving autostart parameters: {}",
    "lbl_local": "Local Path:",
    "lbl_cloud": "Cloud Path:",
    "lbl_autostart": "Autostart Parameters:",
    "btn_sync": "Sync",
    "chkbx_autostart": "Autostart",
    "btn_local": "SetLP",
    "btn_cloud": "SetCP",
    "btn_autostart": "SetAP",
    "tray_open": "Open GUI",
    "tray_exit": "Exit",
    "tray_sync": "Sync now",
    "delay_start": "Delayed start (-d): waiting 5 minutes for the first synchronization...",
    "block_autosync": "Automatic synchronization disabled by parameter.",
    "placeholder_local": "local_saves_path",
    "placeholder_cloud": "cloud_saves_path",
    "placeholder_blacklist": "world1, world 2, world3",
    "btn_blacklist": "SetBL",
    "lbl_blacklist": "Blacklist of Worlds",
    "exit_waiting": "Waiting for the current synchronization to finish before exiting...",
    "config_corrupt": "The configuration file was corrupted. It has been saved as 'config.json.corrupto' and a new one has been created.",
    "temp_cleaned": "Removed leftover temporary file: {}",
    "temp_restored": "Restored world '{}' from an interrupted synchronization.",
    "mc_opened_abort": "Minecraft has been opened during the synchronization. The remaining worlds have been skipped.",
    "dry_mode_active": "Simulation mode (-dr) active: no files will be modified.",
    "auto_updated": "Autostart file updated with the new parameters.",
    "extract_no_level": "the extracted world does not contain level.dat",
    "interval_int_error": "-i '{}' must be an integer.",
    "interval_range_error": "-i '{} must be greater than 0.",
    "autostart_error": "Error applying autostart.",
    "error_local": "The local route cannot be empty.",
    "error_cloud": "The cloud route cannot be empty."
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
    "help_block": "Bloquea la función de autosincronización",
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
    "upload_success": "El mundo '{}' está en la carpeta local de la nube. Revise el cliente de la nube para ver el progreso de la subida.",
    "download_success": "El mundo '{}' ha sido descargado y copiado en local con éxito.",
    "err_unexpected": "Error inesperado: {}",
    "lock_active": "Otro dispositivo está sincronizando ahora mismo (lock activo). Omitiendo...",
    "lock_obsolete": "Se encontró un bloqueo obsoleto. Ignorando...",
    "lock_error": "No se pudo crear el archivo lock: {}",
    "lock_wait": "Finalizando... Esperando 30 segundos para liberar el bloqueo.",
    "corrupt_cloud_skip": "Aviso: El archivo de la nube {}.zip está corrupto o incompleto. Omitiendo.",
    "corrupt_cloud_cancel": "Aviso: El archivo de la nube {}.zip está corrupto o incompleto. Se cancela la sobreescritura.",
    "conflict_both": "¡CONFLICTO! El mundo '{}' ha sido modificado tanto en local como en la nube.",
    "conflict_backup": "Creando copia de seguridad local...",
    "conflict_renamed": "Copia local guardada como '{}' (no se sincronizará). Se ha descargado la versión de la nube.",
    "conflict_dry": "¡CONFLICTO (Dry Run)! El mundo '{}' tiene cambios locales y en la nube.",
    "auto_enabled": "Autoarranque activado en el sistema.",
    "auto_disabled": "Autoarranque desactivado.",
    "tray_sync": "Sincronizar ahora",
    "tray_auto": "Autoarranque",
    "tray_exit": "Salir",
    "tray_title": "Minecraft Sync",
    "sync_in_progress": "Ya hay una sincronización en curso, omitiendo...",
    "mc_running": "No se puede sincronizar: Minecraft se encuentra en ejecución.",
    "saving_start_parameters": "Guardando parámetros de autoarranque: {}",
    "lbl_local": "Ruta Local:",
    "lbl_cloud": "Ruta Nube:",
    "lbl_autostart": "Parámetros Autoarranque:",
    "btn_sync": "Sincronizar",
    "chkbx_autostart": "Autoarranque",
    "btn_local": "GuardarRL",
    "btn_cloud": "GuardarRN",
    "btn_autostart": "GuardarPA",
    "tray_open": "Abrir interfaz",
    "tray_exit": "Salir",
    "tray_sync": "Sincronizar ahora",
    "delay_start": "Inicio con retraso (-d): esperando 5 minutos para la primera sincronización...",
    "block_autosync": "Sincronización automática desactivada por parámetro.",
    "placeholder_local": "ruta_local_de_los_mundos",
    "placeholder_cloud": "ruta_local_de_la_nube",
    "placeholder_blacklist": "mundo1, mundo 2, mundo3",
    "btn_blacklist": "GuardarLN",
    "lbl_blacklist": "Lista Negra de Mundos",
    "exit_waiting": "Esperando a que termine la sincronización en curso antes de salir...",
    "config_corrupt": "El archivo de configuración estaba corrupto. Se ha guardado como 'config.json.corrupto' y se ha creado uno nuevo.",
    "temp_cleaned": "Eliminado archivo temporal sobrante: {}",
    "temp_restored": "Restaurado el mundo '{}' de una sincronización interrumpida.",
    "mc_opened_abort": "Minecraft se ha abierto durante la sincronización. Se han omitido los mundos restantes.",
    "dry_mode_active": "Modo simulación (-dr) activo: no se modificará ningún archivo.",
    "auto_updated": "Archivo de autoarranque actualizado con los nuevos parámetros.",
    "extract_no_level": "el mundo extraído no contiene level.dat",
    "interval_int_error": "-i '{}' debe de ser un número entero.",
    "interval_range_error": "-i '{} debe de ser mayor que 0.",
    "autostart_error": "Error al aplicar el autoarranque.",
    "error_local": "La ruta local no puede estar vacia.",
    "error_cloud": "la ruta de la nube no puede estar vacia."
  }
}

DIRECTORIO_SCRIPT = Path(__file__).parent

def obtener_directorio_config():
  """Devuelve la carpeta de configuración del usuario según el SO (sobrevive a las actualizaciones)"""
  if sys.platform == "win32":
    base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    return base / "MSSync"
  base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
  return base / "mssync"

ARCHIVO_CONFIG = obtener_directorio_config() / "config.json"
# Ubicación usada por versiones anteriores (junto al script o en _internal si está compilado)
ARCHIVO_CONFIG_ANTIGUO = DIRECTORIO_SCRIPT / "config.json"

# Cerrojo para que la ventana y el hilo de sincronización no escriban a la vez
_cerrojo_config = threading.RLock()
_config_corrupta = False

# Variable global para el idioma por defecto
idioma_actual = "en"

def t(clave):
  """Función que devuelve el texto traducido"""
  return TEXTOS.get(idioma_actual, TEXTOS["en"]).get(clave, clave)

def migrar_config_antigua():
  """Copia el config.json de la ubicación antigua a la nueva si todavía no existe"""
  if ARCHIVO_CONFIG.exists() or not ARCHIVO_CONFIG_ANTIGUO.exists():
    return
  try:
    ARCHIVO_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ARCHIVO_CONFIG_ANTIGUO, ARCHIVO_CONFIG)
  except OSError:
    pass

def leer_config():
  """Lee config.json. Si está corrupto lo aparta y devuelve una configuración vacía"""
  global _config_corrupta
  with _cerrojo_config:
    migrar_config_antigua()
    if not ARCHIVO_CONFIG.exists():
      return {}
    try:
      with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
      return datos if isinstance(datos, dict) else {}
    except (json.JSONDecodeError, UnicodeDecodeError):
      # Guardamos el archivo dañado para no perderlo y seguimos con uno vacío
      try:
        os.replace(ARCHIVO_CONFIG, ARCHIVO_CONFIG.with_name("config.json.corrupto"))
      except OSError:
        pass
      _config_corrupta = True
      return {}

def guardar_config(datos):
  """Guarda config.json de forma atómica (archivo local, no afecta a la nube)"""
  with _cerrojo_config:
    ARCHIVO_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    ruta_temporal = ARCHIVO_CONFIG.with_name("config.json.tmp")
    with open(ruta_temporal, "w", encoding="utf-8") as archivo:
      json.dump(datos, archivo, indent=2)
      archivo.flush()
      os.fsync(archivo.fileno())
    os.replace(ruta_temporal, ARCHIVO_CONFIG)

def actualizar_config(clave, valor):
  """Relee la configuración, cambia solo una clave y la guarda"""
  with _cerrojo_config:
    datos = leer_config()
    datos[clave] = valor
    guardar_config(datos)

def actualizar_estado_mundo(mundo, tiempo_local, tiempo_nube):
  """Guarda las fechas de la última sincronización de un mundo sin tocar el resto de la configuración"""
  with _cerrojo_config:
    datos = leer_config()
    if "estado_sync" not in datos:
      datos["estado_sync"] = {}
    datos["estado_sync"][mundo] = {
      "local": int(tiempo_local),
      "nube": int(tiempo_nube)
    }
    guardar_config(datos)

def hubo_config_corrupta():
  """Indica si al arrancar se encontró un config.json corrupto"""
  return _config_corrupta

def validar_ruta(ruta_texto):
  """
  Limpia la ruta y comprueba si es un texto válido y si la carpeta existe.
  Devuelve la ruta limpia si es válida, o None si hay algún problema.
  """
  ruta_limpia = ruta_texto.strip() # Quitamos espacios al principio y al final
  if not ruta_limpia:
    return None
    
  ruta_obj = Path(ruta_limpia)
  if not ruta_obj.exists() or not ruta_obj.is_dir():
    return None
    
  return ruta_limpia

def pre_cargar_idioma():
  """Carga el idioma antes de configurar argparse para traducir el menú de ayuda"""
  global idioma_actual
  datos = leer_config()
  if datos.get("idioma") in TEXTOS:
    idioma_actual = datos["idioma"]

def cargar_configuracion():
  """Carga la configuración del programa desde el archivo config.json"""
  datos = leer_config()
  
  if "ruta_local" not in datos or "ruta_nube" not in datos:
    return None

  ruta_local = validar_ruta(datos["ruta_local"])
  ruta_nube = validar_ruta(datos["ruta_nube"])

  # Si alguna de las rutas no es válida o no existe, abortamos la carga
  if not ruta_local or not ruta_nube:
    return None

  # Además comprobamos que no pongan la misma carpeta en local y nube
  if Path(ruta_local).resolve() == Path(ruta_nube).resolve():
    return None

  config = {
    "ruta_local": Path(datos["ruta_local"]),
    "ruta_nube": Path(datos["ruta_nube"]),
    "blacklist": datos.get("blacklist", []),
    "estado_sync": datos.get("estado_sync", {})
  }

  return config

def establecer_idioma(nuevo_idioma):
  """Actualiza la variable global de idioma en tiempo de ejecución"""
  global idioma_actual
  if nuevo_idioma in TEXTOS:
    idioma_actual = nuevo_idioma