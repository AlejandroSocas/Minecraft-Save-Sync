import argparse
from pathlib import Path
import json
import shutil
import sys

DIRECTORIO_SCRIPT = Path(__file__).parent
ARCHIVO_CONFIG = DIRECTORIO_SCRIPT / "config.json"

# Carga la configuración del programa desde el archivo config.json
def cargar_configuracion():
  try:
    with open(ARCHIVO_CONFIG, "r") as archivo:
      datos = json.load(archivo)
  except FileNotFoundError:
    print("No se ha encontrado el archivo de configuración")
    return None
  
  if "ruta_local" not in datos or "ruta_nube" not in datos:
    print("Error: El archivo de configuración está incompleto. Configura ambas rutas primero.")
    return None

  config = {
    "ruta_local": Path(datos["ruta_local"]),
    "ruta_nube": Path(datos["ruta_nube"]),
    "blacklist": []
  }

  if "blacklist" in datos:
    config["blacklist"] = datos["blacklist"]

  return config

# Comprueba si una ruta pasada existe o no
def existe_ruta(ruta):
  if not ruta.exists():
    print(f"La ruta {ruta} no existe")
    return False
  else:
    return True

def main():
  parser = argparse.ArgumentParser(description="Sincronizador de mundos de Minecraft")
  parser.add_argument("comando", choices=["sync"], nargs="?", help="Sincroniza los mundos locales y en la nube")
  parser.add_argument("-slp", "--setlocalp", help="Establece la ruta local de los mundos")
  parser.add_argument("-scp", "--setcloudp", help="Establece la ruta de la nube de los mundos")
  parser.add_argument("-dr", "--dry-run", action="store_true", help="Realiza una simulación de lo que haría la sincronización pero sin hacerla")
  parser.add_argument("-bla", "--blacklist-add", nargs='+', help="Agrega uno o más elementos a la lista negra")
  parser.add_argument("-blr", "--blacklist-remove", nargs='+', help="Elimina uno o más elementos de la lista negra")
  
  # Cargamos los datos previos si existen
  datos = {}
  if ARCHIVO_CONFIG.exists():
    with open(ARCHIVO_CONFIG, "r") as archivo:
      datos = json.load(archivo)
  
  guardar_json = False

  # Control de los argumentos de la línea de comandos
  args = parser.parse_args()

  # Añade elementos a la blacklist
  if args.blacklist_add:
    for mundo in args.blacklist_add:
      if not "blacklist" in datos:
        datos["blacklist"] = []
      if mundo in datos["blacklist"]:
        print(f"El mundo '{mundo}' ya estaba en la blacklist")
      else:
        datos["blacklist"].append(mundo)
        print(f"Se ha añadido el mundo '{mundo}' a la lista negra")
        guardar_json = True
  
  if args.blacklist_remove:
    if "blacklist" in datos and datos["blacklist"]:
      for mundo in args.blacklist_remove:
        if mundo in datos["blacklist"]:
          datos["blacklist"].remove(mundo)
          print(f"Se ha quitado el mundo '{mundo}' de la lista negra")
        else:
          print(f"El mundo '{mundo}' no estaba en la lista negra")
        guardar_json = True
    else:
      print("La blacklist está vacía")
  
  # Sincronización
  if args.comando == "sync" or args.dry_run:
    if not args.dry_run:
      print("Iniciando sincronización...")
    else:
      print("Iniciando simulación (dry run)")
    rutas = cargar_configuracion()

    # Comprobamos si se ha cargado todo correctamente y si las rutas existen
    if not rutas:
      print("Sincronización abortada")
      sys.exit(1)
    if not existe_ruta(rutas["ruta_local"]) or not existe_ruta(rutas["ruta_nube"]):
      print("Sincronización abortada")
      sys.exit(2)

    # Obtenemos todos los mundos locales y en la nube
    mundos_locales = [mundo.name for mundo in rutas["ruta_local"].iterdir() if mundo.is_dir()]
    mundos_nube = [mundo.name for mundo in rutas["ruta_nube"].iterdir() if mundo.is_dir()]

    # Miramos a ver los mundos locales que no están en la nube
    for mundo in mundos_locales[:]:
      # Comprobación de blacklist
      if mundo in rutas["blacklist"]:
        continue
      if not mundo in mundos_nube:
        mundos_locales.remove(mundo)
        print(f"Subiendo mundo nuevo a la nube: {mundo}")
        # Copiar local a nube
        ruta_mundo_local = Path(rutas["ruta_local"] / mundo)
        ruta_mundo_nube = Path(rutas["ruta_nube"] / mundo)
        if not args.dry_run: 
          shutil.copytree(ruta_mundo_local, ruta_mundo_nube)
        else:
          print(f"Se ha copiado el mundo [{ruta_mundo_local}] en la nube [{ruta_mundo_nube}]")
    
    # Miramos a ver los mundos en la nube que no están en local
    for mundo in mundos_nube[:]:
      # Comprobación de blacklist
      if mundo in rutas["blacklist"]:
        continue
      if not mundo in mundos_locales:
        mundos_nube.remove(mundo)
        print(f"Descargando mundo nuevo a local: {mundo}")
        # Copiar de nube a local
        ruta_mundo_local = Path(rutas["ruta_local"] / mundo)
        ruta_mundo_nube = Path(rutas["ruta_nube"] / mundo)
        if not args.dry_run:
          shutil.copytree(ruta_mundo_nube, ruta_mundo_local)
        else:
          print(f"Se ha copiado de la nube [{ruta_mundo_nube}] al directorio local [{ruta_mundo_local}]")
    
    # Si los mundos están en los dos lados comprobamos cual se ha modificado más recientemente
    for mundo in mundos_locales:
      # Comprobación de blacklist
      if mundo in rutas["blacklist"]:
        continue
      ruta_mundo_local = Path(rutas["ruta_local"] / mundo)
      ruta_mundo_nube = Path(rutas["ruta_nube"] / mundo)
      level_local = ruta_mundo_local / "level.dat"
      level_nube = ruta_mundo_nube / "level.dat"
      if level_local.exists() and level_nube.exists():
        tiempo_modificado_local = level_local.stat().st_mtime
        tiempo_modificado_nube = level_nube.stat().st_mtime
        if tiempo_modificado_local > tiempo_modificado_nube:
          # Sobreescribir el local en la nube
          if not args.dry_run:
            print(f"Sobrescribiendo la nube con la versión local de {mundo}...")
            shutil.rmtree(ruta_mundo_nube)
            shutil.copytree(ruta_mundo_local, ruta_mundo_nube)
          else:
            print(f"Se ha sobreescrito el mundo en la nube [{ruta_mundo_nube}] con la versión local de [{ruta_mundo_local}]")
        elif tiempo_modificado_nube > tiempo_modificado_local:
          # Sobreescribir sobreescribir el de la nube en local
          if not args.dry_run:
            print(f"Sobrescribiendo local con la versión de la nube de {mundo}...")
            shutil.rmtree(ruta_mundo_local)
            shutil.copytree(ruta_mundo_nube, ruta_mundo_local)
          else:
            print(f"Se ha sobreescrito el mundo en local [{ruta_mundo_local}] con la versión en la nube [{ruta_mundo_nube}]")
        else:
          if not args.dry_run:
            print(f"El mundo {mundo} se encuentra ya sincronizado")
          else:
            print(f"No ha ocurrido nada porque las dos versiones del mundo '{mundo}' estaban correctamente sincronizadas")
      else:
        print(f"Aviso: El mundo {mundo} parece estar corrupto o no tiene level.dat")
  
  # Establece la ruta local de guardado
  if args.setlocalp:
    print(f"Guardando nueva ruta local: {args.setlocalp}")
    datos["ruta_local"] = args.setlocalp
    guardar_json = True

  # Establece la ruta de guardado en la nube
  if args.setcloudp:
    print(f"Guardando nueva ruta de la nube: {args.setcloudp}")
    datos["ruta_nube"] = args.setcloudp # Guardamos directamente el string
    guardar_json = True
  
  # Guardamos la configuración solo si hubo algún cambio
  if guardar_json:
    with open(ARCHIVO_CONFIG, "w") as archivo:
      json.dump(datos, archivo, indent=2)
  
  sys.exit(0)

if __name__ == "__main__":
  main()