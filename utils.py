import psutil
import zipfile
import sys

from config import *


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


def alternar_autoarranque(activar):
  """Activa/desactiva el autoarranque del programa al iniciar el SO"""
  ruta = obtener_ruta_autoarranque()
  if not ruta:
    return
  
  # Si nos piden desactivarlo y existe, lo borramos
  if not activar:
    if ruta.exists():
      ruta.unlink()
    return

  # Si nos piden activarlo
  ruta.parent.mkdir(parents=True, exist_ok=True)
  
  # Leemos los parámetros personalizados que el usuario guardó
  parametros = ""
  if ARCHIVO_CONFIG.exists():
    with open(ARCHIVO_CONFIG, "r") as archivo:
      datos = json.load(archivo)
      parametros = datos.get("parametros_autoarranque", "")

  if getattr(sys, 'frozen', False):
    comando = f'"{sys.executable}" {parametros}'.strip()
  else:
    comando = f'"{sys.executable}" "{Path(__file__).resolve().parent / "main.py"}" {parametros}'.strip()
  
  if sys.platform.startswith('linux'):
    contenido = f"[Desktop Entry]\nType=Application\nExec={comando}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName=Minecraft Sync Tray\n"
    ruta.write_text(contenido)
  elif sys.platform == "win32":
    ruta.write_text(f'@echo off\nstart "" /b {comando}\n')


def zip_es_valido(ruta_zip):
  """Comprueba si un archivo zip está corrupto o incompleto"""
  try:
    with zipfile.ZipFile(ruta_zip, 'r') as z:
      # testzip() devuelve el nombre del primer archivo corrupto, o None si todo está bien
      if z.testzip() is not None:
        return False
      
      # Comprobación extra: Verificar que el nivel base (level.dat) existe dentro del zip
      # Esto evita que se extraiga un mundo vacío o a medias
      archivos = z.namelist()
      
      # level.dat puede estar en la raíz o dentro de una subcarpeta, comprobamos si alguna ruta lo contiene
      if not any(archivo.endswith("level.dat") for archivo in archivos):
        return False
        
    return True
  except zipfile.BadZipFile:
    return False
