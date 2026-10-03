import argparse
import sys

from sync_core import *
from gui import *

def main():

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
  parser.add_argument("-b", "--block-autosync", action="store_true", help=t("help_block"))
  
  args = parser.parse_args()

  # Leemos la configuración para procesar argumentos de configuración antes de sincronizar
  datos = leer_config()
  
  guardar_json_main = False

  # Cambiamos el idioma
  if args.lang:
    establecer_idioma(args.lang)
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
    guardar_config(datos)
  
  # Arrancamos la GUI
  app = QApplication(sys.argv)
  
  # Prevenir que la app se cierre si cerramos la ventana principal
  app.setQuitOnLastWindowClosed(False)
  
  # Instanciamos la ventana pasándole los argumentos
  ventana = Ventana(args)
  
  # Decidimos cómo mostrar el programa según los argumentos
  if args.tray:
    # Si se arranca con --tray, no hacemos ventana.show(), se queda oculto
    pass
  else:
    ventana.show()
    
    # Si el usuario ejecutó "python mssync.py sync" desde la terminal,
    # abrimos la ventana e iniciamos la sincronización automáticamente.
    if args.comando == "sync" or args.dry_run:
      ventana.empezar_sincronizacion()
  
  # Iniciamos el bucle de eventos de Qt
  sys.exit(app.exec())

if __name__ == "__main__":
  main()