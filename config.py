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