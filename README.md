# Minecraft-Save-Sync

Script de Python por CLI que se encarga de sincronizar los mundos de Minecraft entre una carpeta local y un directorio en la nube. Es teóricamente compatible con Linux, Windows y MacOS, aunque actualmente solo ha sido testeado de forma exhaustiva en entornos Linux.

## Cuidado
Este script utiliza operaciones de sobrescritura y borrado (`shutil`). Se recomienda encarecidamente **hacer una copia de seguridad manual** de tus mundos antes de usar la herramienta por primera vez, para evitar pérdidas de progreso en caso de configurar las rutas incorrectamente.

## Prerrequisitos
Este programa utiliza únicamente librerías estándar de Python, por lo que no es necesario instalar dependencias externas. Solo necesitas:
* Python 3.6 o superior.

## Instalación

Tienes dos opciones para descargar y preparar la herramienta en tu equipo:

**Opción A: Usando Git (Recomendado)**
1. Abre tu terminal y clona el repositorio:
  ```bash
  git clone https://github.com/AlejandroSocas/Minecraft-Save-Sync.git
  ```

2. Navega hasta la carpeta recién descargada:
  ```bash
  cd Minecraft-Save-Sync
  ```

**Opción B: Descarga manual (Sin Git)**

Haz clic en el botón verde "<> Code" en la parte superior derecha de esta página y selecciona "Download ZIP".

Descomprime el archivo descargado en la carpeta donde desees guardar el programa.

Abre una terminal y navega hasta esa carpeta (ej: cd Descargas/Minecraft-Save-Sync).

## Uso general

En la terminal de tu sistema operativo dentro de la carpeta donde instalastes el programa:

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

### Automatización con Prism Launcher (Opcional)

Puedes configurar Prism Launcher para que sincronice tus mundos automáticamente cada vez que cierres el juego, abriendo una terminal para que puedas ver el proceso.

1. Haz clic derecho en tu instancia de Minecraft y selecciona **Editar instancia**.
2. Ve a **Configuraciones > Comandos personalizados**.
3. Marca la casilla para habilitar los comandos.
4. En el campo **Comando posterior a la ejecución**, pega el comando correspondiente a tu sistema operativo (recuerda cambiar la ruta por la ubicación real de tu script):

**Windows:**
`start cmd /k "python C:\"ruta"\mssync.py sync"`

**Linux (GNOME):**
`gnome-terminal -- bash -c "python /"ruta"/mssync.py sync; echo ''; read -p 'Presiona Enter para cerrar...'"`

**Linux (KDE):**
`konsole -e bash -c "python /"ruta"/mssync.py sync; echo ''; read -p 'Presiona Enter para cerrar...'"`

***¡Recuerda cambiar "ruta" por la ruta real donde instalastes el programa!***