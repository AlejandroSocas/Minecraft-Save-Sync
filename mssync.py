import argparse
from pathlib import Path
import json
import shutil
import sys

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
    "critic_error": "Critical error during copying {}: {}"
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
    "critic_error": "Error crítico durante la copia de {}: {}"
  }
}

# Función que devuelve el texto traducido
def t(clave):
  return TEXTOS.get(idioma_actual, TEXTOS["en"]).get(clave, clave)

# Carga el idioma antes de configurar argparse para traducir el menú de ayuda
def pre_cargar_idioma():
  global idioma_actual
  if ARCHIVO_CONFIG.exists():
    try:
      with open(ARCHIVO_CONFIG, "r") as archivo:
        datos = json.load(archivo)
        if "idioma" in datos:
          idioma_actual = datos["idioma"]
    except json.JSONDecodeError:
      pass

# Carga la configuración del programa desde el archivo config.json
def cargar_configuracion():
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

def main():
  global idioma_actual
  
  # Leemos el config.json por adelantado solo para saber en qué idioma pintar argparse
  pre_cargar_idioma()

  parser = argparse.ArgumentParser(description=t("desc"))
  parser.add_argument("comando", choices=["sync"], nargs="?", help=t("help_sync"))
  parser.add_argument("-slp", "--setlocalp", help=t("help_slp"))
  parser.add_argument("-scp", "--setcloudp", help=t("help_scp"))
  parser.add_argument("-dr", "--dry-run", action="store_true", help=t("help_dr"))
  parser.add_argument("-bla", "--blacklist-add", nargs='+', help=t("help_bla"))
  parser.add_argument("-blr", "--blacklist-remove", nargs='+', help=t("help_blr"))
  parser.add_argument("-l", "--lang", choices=["en", "es"], help=t("help_lang"))
  
  # Cargamos los datos previos si existen
  datos = {}
  if ARCHIVO_CONFIG.exists():
    with open(ARCHIVO_CONFIG, "r") as archivo:
      datos = json.load(archivo)
  
  guardar_json = False

  # Control de los argumentos de la línea de comandos
  args = parser.parse_args()

  # Aplicamos el cambio de idioma inmediatamente si el usuario usa el flag
  if args.lang:
    idioma_actual = args.lang
    datos["idioma"] = args.lang
    print(t("saving_lang").format(args.lang))
    guardar_json = True

  # Añade elementos a la blacklist
  if args.blacklist_add:
    for mundo in args.blacklist_add:
      if not "blacklist" in datos:
        datos["blacklist"] = []
      if mundo in datos["blacklist"]:
        print(t("bl_already").format(mundo))
      else:
        datos["blacklist"].append(mundo)
        print(t("bl_added").format(mundo))
        guardar_json = True
  
  if args.blacklist_remove:
    if "blacklist" in datos and datos["blacklist"]:
      for mundo in args.blacklist_remove:
        if mundo in datos["blacklist"]:
          datos["blacklist"].remove(mundo)
          print(t("bl_removed").format(mundo))
        else:
          print(t("bl_not_in").format(mundo))
        guardar_json = True
    else:
      print(t("bl_empty"))
  
  # Sincronización
  if args.comando == "sync" or args.dry_run:
    if not args.dry_run:
      print(t("sync_init"))
    else:
      print(t("sync_dry"))
    
    rutas = cargar_configuracion()

    # Comprobamos si se ha cargado todo correctamente y si las rutas existen
    if not rutas:
      print(t("sync_abort"))
      sys.exit(1)
    if not existe_ruta(rutas["ruta_local"]) or not existe_ruta(rutas["ruta_nube"]):
      print(t("sync_abort"))
      sys.exit(2)

    # Obtenemos todos los mundos locales y en la nube
    mundos_locales = [mundo.name for mundo in rutas["ruta_local"].iterdir() if mundo.is_dir()]
    mundos_nube = [mundo.name for mundo in rutas["ruta_nube"].iterdir() if mundo.is_dir()]

    # Miramos a ver los mundos locales que no están en la nube
    for mundo in mundos_locales[:]:
      # Comprobación de blacklist (Ahora protegido usando 'rutas')
      if mundo in rutas["blacklist"]:
        continue
      if not mundo in mundos_nube:
        mundos_locales.remove(mundo)
        print(t("upload_new").format(mundo))
        # Copiar local a nube
        ruta_mundo_local = Path(rutas["ruta_local"] / mundo)
        ruta_mundo_nube = Path(rutas["ruta_nube"] / mundo)
        
        # Captura de excepciones para proteger el proceso de copia de mundos
        try:
          if not args.dry_run: 
            shutil.copytree(ruta_mundo_local, ruta_mundo_nube)
            
            # Registro de Estado Inicial mtime
            level_local = ruta_mundo_local / "level.dat"
            level_nube = ruta_mundo_nube / "level.dat"
            
            if level_local.exists() and level_nube.exists():
              if "estado_sync" not in datos: 
                datos["estado_sync"] = {}
              
              datos["estado_sync"][mundo] = {
                "local": level_local.stat().st_mtime,
                "nube": level_nube.stat().st_mtime
              }
              guardar_json = True
            
          else:
            print(t("upload_dry").format(ruta_mundo_local, ruta_mundo_nube))
        except Exception as e:
          print(t("critic_error").format(mundo, e))
          continue
    
    # Miramos a ver los mundos en la nube que no están en local
    for mundo in mundos_nube[:]:
      # Comprobación de blacklist (Ahora protegido usando 'rutas')
      if mundo in rutas["blacklist"]:
        continue
      if not mundo in mundos_locales:
        mundos_nube.remove(mundo)
        print(t("download_new").format(mundo))
        # Copiar de nube a local
        ruta_mundo_local = Path(rutas["ruta_local"] / mundo)
        ruta_mundo_nube = Path(rutas["ruta_nube"] / mundo)
        
        # Captura de excepciones para proteger el proceso de copia de mundos
        try:
          if not args.dry_run:
            shutil.copytree(ruta_mundo_nube, ruta_mundo_local)
            
            # Registro de Estado Inicial mtime
            level_local = ruta_mundo_local / "level.dat"
            level_nube = ruta_mundo_nube / "level.dat"
            
            if level_local.exists() and level_nube.exists():
              if "estado_sync" not in datos: 
                datos["estado_sync"] = {}
              
              datos["estado_sync"][mundo] = {
                "local": level_local.stat().st_mtime,
                "nube": level_nube.stat().st_mtime
              }
              guardar_json = True
            
          else:
            print(t("download_dry").format(ruta_mundo_nube, ruta_mundo_local))
        except Exception as e:
          print(t("critic_error").format(mundo, e))
          continue
    
    # Si los mundos están en los dos lados comprobamos cual se ha modificado más recientemente
    for mundo in mundos_locales:
      # Comprobación de si el mundo está en la blacklist
      if mundo in rutas["blacklist"]:
        continue
      
      ruta_mundo_local = Path(rutas["ruta_local"] / mundo)
      ruta_mundo_nube = Path(rutas["ruta_nube"] / mundo)
      level_local = ruta_mundo_local / "level.dat"
      level_nube = ruta_mundo_nube / "level.dat"
      
      if level_local.exists() and level_nube.exists():
        tiempo_modificado_local = level_local.stat().st_mtime
        tiempo_modificado_nube = level_nube.stat().st_mtime
        
        # Recuperamos las fechas del último sync (si no existen, asumimos 0)
        estado_anterior = rutas["estado_sync"].get(mundo, {"local": 0, "nube": 0})
        ultimo_local_conocido = estado_anterior["local"]
        ultima_nube_conocida = estado_anterior["nube"]
        
        # Comprobación de si ha cambiado el tiempo
        local_ha_cambiado = tiempo_modificado_local > ultimo_local_conocido
        nube_ha_cambiado = tiempo_modificado_nube > ultima_nube_conocida

        if local_ha_cambiado:
          # Si local cambió, seguro que jugamos aquí. Subimos a la nube ignorando el mtime de la nube.
          try:
            if not args.dry_run:
              print(t("overwrite_cloud").format(mundo))
              shutil.rmtree(ruta_mundo_nube)
              shutil.copytree(ruta_mundo_local, ruta_mundo_nube)
              # Guardamos las nuevas fechas
              if "estado_sync" not in datos: datos["estado_sync"] = {}
              datos["estado_sync"][mundo] = {
                "local": tiempo_modificado_local,
                # Leemos la fecha real que el SO le dio al archivo recién copiado en la nube
                "nube": (ruta_mundo_nube / "level.dat").stat().st_mtime 
              }
              guardar_json = True
            else:
              print(t("overwrite_cloud_dry").format(ruta_mundo_nube, ruta_mundo_local))
          except Exception as e:
            print(t("critic_error").format(mundo, e))
            continue
        
        elif nube_ha_cambiado and not local_ha_cambiado:
          # Si la nube cambió pero local está intacto, alguien jugó en otro PC (o la nube se actualizó sola).
          # Descargamos sin miedo.
          try:
            if not args.dry_run:
              print(t("overwrite_local").format(mundo))
              shutil.rmtree(ruta_mundo_local)
              shutil.copytree(ruta_mundo_nube, ruta_mundo_local)
              # Guardamos las nuevas fechas
              if "estado_sync" not in datos: datos["estado_sync"] = {}
              datos["estado_sync"][mundo] = {
                "local": (ruta_mundo_local / "level.dat").stat().st_mtime,
                "nube": tiempo_modificado_nube
              }
              guardar_json = True
            else:
              print(t("overwrite_local_dry").format(ruta_mundo_local, ruta_mundo_nube))
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
  
  # Establece la ruta local de guardado
  if args.setlocalp:
    print(t("saving_local").format(args.setlocalp))
    datos["ruta_local"] = args.setlocalp
    guardar_json = True

  # Establece la ruta de guardado en la nube
  if args.setcloudp:
    print(t("saving_cloud").format(args.setcloudp))
    datos["ruta_nube"] = args.setcloudp
    guardar_json = True
  
  # Guardamos la configuración solo si hubo algún cambio
  if guardar_json:
    with open(ARCHIVO_CONFIG, "w") as archivo:
      json.dump(datos, archivo, indent=2)
  
  sys.exit(0)

if __name__ == "__main__":
  main()