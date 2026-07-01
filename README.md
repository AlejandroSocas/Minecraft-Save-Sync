# Minecraft-Save-Sync

Script de Python por CLI que se encarga de sincronizar los mundos de Minecraft entre una carpeta local y un directorio en la nube. Es teóricamente compatible con Linux, Windows y MacOS, aunque actualmente solo ha sido testeado de forma exhaustiva en entornos Linux.

## Cuidado
Este script utiliza operaciones de sobrescritura y borrado (`shutil`). Se recomienda encarecidamente **hacer una copia de seguridad manual** de tus mundos antes de usar la herramienta por primera vez, para evitar pérdidas de progreso en caso de configurar las rutas incorrectamente.

## Prerrequisitos
Este programa utiliza únicamente librerías estándar de Python, por lo que no es necesario instalar dependencias externas. Solo necesitas:
* Python 3.6 o superior.

## Uso general

En la terminal de tu sistema operativo:

```text
mssync.py [-h] [-slp SETLOCALP] [-scp SETCLOUDP] [{sync}]

positional arguments:
  {sync}                Sincroniza los mundos locales y en la nube

options:
  -h, --help            Muestra las opciones del programa
  -slp, --setlocalp SETLOCALP
                        Establece la ruta local de los mundos
  -scp, --setcloudp SETCLOUDP
                        Establece la ruta de la nube de los mundos
```

### Ejemplo de uso
Configuración inicial de las rutas de los mundos (solo se hace la primera vez y queda guardado en config.json)
  ```text
  python mssync.py --setlocalp /home/user/.minecraft/saves/ --setcloudp /home/user/Onedrive/MCSaves/
  ```

Sincronización (Lo haces cada vez que termines de jugar a un mundo )
  ```text
  python mssync.py sync
  ```