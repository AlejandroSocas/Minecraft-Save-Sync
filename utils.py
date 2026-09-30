import psutil

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