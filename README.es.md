# Minecraft-Save-Sync

🌍 *Leer en otros idiomas: [English](README.md), [Español](README.es.md).*

---

Script de Python por CLI bilingüe (Inglés/Español) que se encarga de sincronizar los mundos de Minecraft entre una carpeta local y un directorio en la nube. Es teóricamente compatible con Linux, Windows y MacOS, aunque actualmente solo ha sido testeado de forma exhaustiva en entornos Linux.

## Advertencia
Este script utiliza operaciones de sobrescritura y borrado (`shutil`). Se recomienda encarecidamente **hacer una copia de seguridad manual** de tus mundos antes de usar la herramienta por primera vez, para evitar pérdidas de progreso en caso de configurar las rutas incorrectamente.

## Prerrequisitos
Este programa utiliza únicamente librerías estándar de Python, por lo que no es necesario instalar dependencias externas. Solo necesitas:
* Python 3.6 o superior.
* **Tener tu servicio de nube instalado localmente** (ej. la aplicación de escritorio de OneDrive, Google Drive, Dropbox, etc.), ya que el script funciona interactuando con la carpeta de sincronización local que crean estos servicios en tu disco duro.

## Instalación

Tienes dos opciones para descargar y preparar la herramienta en tu equipo:

**Opción A: Usando Git (Recomendado)**
1. Abre tu terminal y clona el repositorio:
   ```bash
   git clone [https://github.com/AlejandroSocas/Minecraft-Save-Sync.git](https://github.com/AlejandroSocas/Minecraft-Save-Sync.git)
   ```

2. Navega hasta la carpeta recién descargada:
   ```bash
   cd Minecraft-Save-Sync
   ```

**Opción B: Descarga manual (Sin Git)**
1. Haz clic en el botón verde "<> Code" en la parte superior derecha de esta página y selecciona "Download ZIP".
2. Descomprime el archivo descargado en la carpeta donde desees guardar el programa.
3. Abre una terminal y navega hasta esa carpeta (ej: `cd Descargas/Minecraft-Save-Sync`).

## Uso general

En la terminal de tu sistema operativo, dentro de la carpeta donde instalaste el programa:

```text
mssync.py [-h] [-slp SETLOCALP] [-scp SETCLOUDP] [-dr] [-bla BLACKLIST_ADD [BLACKLIST_ADD ...]] [-blr BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]] [-l {en,es}] [{sync}]

positional arguments:
  {sync}                Sincroniza los mundos locales y en la nube

options:
  -h, --help            Muestra las opciones del programa
  -slp, --setlocalp SETLOCALP
                        Establece la ruta local de los mundos
  -scp, --setcloudp SETCLOUDP
                        Establece la ruta de la nube de los mundos
  -dr, --dry-run        Realiza una simulación de lo que haría la sincronización pero sin modificar archivos
  -bla, --blacklist-add BLACKLIST_ADD [BLACKLIST_ADD ...]
                        Agrega uno o más mundos a la lista negra
  -blr, --blacklist-remove BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]
                        Elimina uno o más mundos de la lista negra
  -l, --lang {en,es}    Establece el idioma (en/es)
```

## Ejemplos de uso

### 1. Configuración inicial
Establece las rutas de tus mundos. Esto **solo se hace la primera vez** y queda guardado en `config.json`.
```bash
python mssync.py --setlocalp /home/user/.minecraft/saves/ --setcloudp /home/user/Onedrive/MCSaves/
```

### 2. Sincronización
Ejecuta este comando cada vez que termines de jugar a un mundo para actualizar la nube.
```bash
python mssync.py sync
```

### 3. Simulación (Dry Run)
Si quieres comprobar qué mundos se subirían, bajarían o sobrescribirían sin realizar ningún cambio real en tus archivos, añade el parámetro `-dr`.
```bash
python mssync.py sync -dr
```

### 4. Gestión de la Lista Negra (Blacklist)
Si tienes mundos de prueba pesados que no quieres sincronizar con la nube, puedes añadirlos a la lista negra. El programa los ignorará de forma automática y permanente en cada sincronización hasta que decidas eliminarlos de la lista.

Añadir mundos:
```bash
python mssync.py -bla "Mundo Pruebas" "Mundo Hardcore"
```

Quitar mundos:
```bash
python mssync.py -blr "Mundo Pruebas"
```

### 5. Cambio de Idioma
El programa funciona en inglés por defecto. Puedes cambiar la interfaz al español permanentemente con un solo comando:
```bash
python mssync.py -l es
```

## Automatización con Prism Launcher (Opcional)

Puedes configurar Prism Launcher para que sincronice tus mundos automáticamente cada vez que cierres el juego, abriendo una terminal para que puedas ver el proceso.

1. Haz clic derecho en tu instancia de Minecraft y selecciona **Editar instancia**.
2. Ve a **Configuraciones > Comandos personalizados**.
3. Marca la casilla para habilitar los comandos.
4. En el campo **Comando posterior a la ejecución**, pega el comando correspondiente a tu sistema operativo:

**Windows:**
`cmd /c start cmd /k "python C:\ruta\a\mssync.py sync"`

**Linux (GNOME):**
`gnome-terminal -- bash -c "python /ruta/mssync.py sync; echo ''; read -p 'Presiona Enter para cerrar...'"`

**Linux (KDE):**
`konsole -e bash -c "python /ruta/mssync.py sync; echo ''; read -p 'Presiona Enter para cerrar...'"`

***¡Recuerda cambiar "ruta" por la ruta absoluta real donde instalaste el programa!***