# Minecraft-Save-Sync

🌍 *Leer en otros idiomas: [English](README.md), [Español](README.es.md).*

---

Script de Python bilingüe (Inglés/Español) que se encarga de sincronizar mundos de Minecraft entre una carpeta local y un directorio en la nube. Puede utilizarse mediante línea de comandos (CLI) o ejecutarse en segundo plano en la bandeja del sistema (*System Tray*). Comprime automáticamente cada mundo en archivos `.zip` en la nube para optimizar la velocidad de subida/bajada y proteger la integridad de los archivos. Compatible con Windows y Linux.

## Advertencia
Este script utiliza operaciones de compresión, sobrescritura y borrado (`shutil`). Se recomienda encarecidamente **hacer una copia de seguridad manual** de tus mundos antes de usar la herramienta por primera vez, para evitar pérdidas de progreso en caso de configurar las rutas incorrectamente.

## Prerrequisitos
* Python 3.6 o superior.
* **Tener tu servicio de nube instalado localmente** (ej. la aplicación de escritorio de Google Drive, OneDrive, Dropbox, etc.), ya que el script funciona interactuando con la carpeta de sincronización local que crean estos servicios en tu disco duro.
* **Dependencias de Python:** Instala las librerías necesarias ejecutando:
  ```bash
  pip install psutil pystray Pillow
  ```
  *(Nota para usuarios de Linux con GNOME: asegúrate de tener instalada y habilitada la extensión "AppIndicator and KStatusNotifierItem Support" para poder visualizar los iconos en la bandeja del sistema).*

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
1. Haz clic en el botón verde "<> Code" en la parte superior derecha de esta página y selecciona "Download ZIP".
2. Descomprime el archivo descargado en la carpeta donde desees guardar el programa.
3. Abre una terminal y navega hasta esa carpeta (ej: `cd Descargas/Minecraft-Save-Sync`).

## Uso general

En la terminal de tu sistema operativo, dentro de la carpeta donde instalaste el programa:

```text
mssync.py [-h] [-slp SETLOCALP] [-scp SETCLOUDP] [-dr]
          [-bla BLACKLIST_ADD [BLACKLIST_ADD ...]]
          [-blr BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]] [-l {en,es}]
          [-t] [-d] [-i INTERVAL]
          [{sync}]

positional arguments:
  {sync}                Sincroniza los mundos locales y en la nube

options:
  -h, --help            Muestra las opciones del programa
  -slp, --setlocalp SETLOCALP
                        Establece la ruta local de los mundos
  -scp, --setcloudp SETCLOUDP
                        Establece la ruta de la nube de los mundos
  -dr, --dry-run        Realiza una simulación de lo que haría la sincronización sin modificar archivos
  -bla, --blacklist-add BLACKLIST_ADD [BLACKLIST_ADD ...]
                        Agrega uno o más mundos a la lista negra
  -blr, --blacklist-remove BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]
                        Elimina uno o más mundos de la lista negra
  -l, --lang {en,es}    Establece el idioma (en/es)
  -t, --tray            Inicia el programa en la bandeja del sistema
  -d, --delay           Retrasa el inicio 5 minutos
  -i, --interval INTERVAL
                        Minutos entre cada sincronización automática (por defecto: 30)
```

## Ejemplos de uso

### 1. Configuración inicial
Establece las rutas de tus mundos. Esto **solo se hace la primera vez** en cada equipo y queda guardado en `config.json`.
```bash
python mssync.py --setlocalp "C:\Users\tu_usuario\AppData\Roaming\.minecraft\saves" --setcloudp "C:\Users\tu_usuario\OneDrive\MundosMC"
```

### 2. Modo Bandeja del Sistema (System Tray / Segundo plano)
Inicia la aplicación residente junto al reloj de tu sistema operativo para sincronizaciones automáticas periódicas:
```bash
python mssync.py --tray
```

Opciones adicionales para el modo tray:
* **Cambiar el intervalo de comprobación** (ej. cada 15 minutos en vez de los 30 por defecto):
  ```bash
  python mssync.py --tray -i 15
  ```
* **Retraso inicial de 5 minutos** (ideal al iniciar sesión para dar tiempo a que tu nube conecte a internet):
  ```bash
  python mssync.py --tray --delay
  ```

**Funciones del menú contextual (clic derecho en el icono):**
* **Sincronizar ahora:** Fuerza una comprobación y sincronización inmediata.
* **Autoarranque:** Casilla interactiva para activar o desactivar que el programa se inicie automáticamente al encender el ordenador (en Windows crea el `.bat` en Startup y en Linux genera el `.desktop` en autostart).
* **Salir:** Detiene el hilo de sincronización y cierra el icono limpiamente.
* *Nota de seguridad:* El programa detecta automáticamente si Minecraft está en ejecución mediante `psutil` y pospondrá cualquier sincronización hasta que cierres el juego para proteger las partidas contra corrupción.

### 3. Sincronización manual por CLI
Si prefieres no usar el tray y sincronizar manualmente en un momento puntual:
```bash
python mssync.py sync
```

### 4. Simulación (Dry Run)
Si quieres comprobar qué mundos se subirían, bajarían o sobrescribirían sin realizar ningún cambio real en tus archivos, añade el parámetro `-dr`.
```bash
python mssync.py sync -dr
```

### 5. Gestión de la Lista Negra (Blacklist)
Si tienes mundos de prueba pesados que no quieres sincronizar con la nube, puedes añadirlos a la lista negra. El programa los ignorará de forma automática y permanente en cada sincronización hasta que decidas eliminarlos de la lista.

Añadir mundos:
```bash
python mssync.py -bla "Mundo Pruebas" "Mundo Hardcore"
```

Quitar mundos:
```bash
python mssync.py -blr "Mundo Pruebas"
```

### 6. Cambio de Idioma
El programa funciona en inglés por defecto. Puedes cambiar la interfaz al español permanentemente con un solo comando:
```bash
python mssync.py -l es
```

## Automatización con Prism Launcher (Opcional)

Si prefieres no tener la aplicación en segundo plano en el tray, puedes configurar Prism Launcher para sincronizar automáticamente al abrir y cerrar el juego:

1. Haz clic derecho en tu instancia de Minecraft y selecciona **Editar instancia**.
2. Ve a **Configuraciones > Comandos personalizados** y marca la casilla para habilitar los comandos.
3. Para descargar las partidas más recientes antes de jugar, en **Comando previo al lanzamiento**:
   * **Windows:** `cmd /c "python C:\ruta\a\mssync.py sync"`
   * **Linux:** `bash -c "python /ruta/mssync.py sync"`
4. Para subir las partidas modificadas al salir, en **Comando posterior a la ejecución**:
   * **Windows:** `cmd /c start cmd /k "python C:\ruta\a\mssync.py sync"`
   * **Linux (GNOME):** `gnome-terminal -- bash -c "python /ruta/mssync.py sync; echo ''; read -p 'Presiona Enter para cerrar...'"`
   * **Linux (KDE):** `konsole -e bash -c "python /ruta/mssync.py sync; echo ''; read -p 'Presiona Enter para cerrar...'"`

***¡Recuerda cambiar "ruta" por la ruta absoluta real donde instalaste el programa!***