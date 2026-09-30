import argparse
from PIL import Image, ImageDraw
import time
import sys

from sync_core import *





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