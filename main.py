import argparse
from PIL import Image, ImageDraw
import time
import sys

from sync_core import *


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