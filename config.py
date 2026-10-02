from pathlib import Path
import json

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
    "conflict_renamed": "Local world renamed to '{}'. The cloud version will now be downloaded.",
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
    "tray_sync": "Sync now"
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
    "conflict_renamed": "Mundo local renombrado a '{}'. Ahora se descargará la versión de la nube.",
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
    "tray_sync": "Sincronizar ahora"
  }
}

DIRECTORIO_SCRIPT = Path(__file__).parent
ARCHIVO_CONFIG = DIRECTORIO_SCRIPT / "config.json"

# Variable global para el idioma por defecto
idioma_actual = "en"

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
    return None
  
  if "ruta_local" not in datos or "ruta_nube" not in datos:
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