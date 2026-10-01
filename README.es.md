# Minecraft-Save-Sync

🌍 *Leer en otros idiomas: [English](README.md), [Español](README.es.md).*

---

Aplicación de escritorio y script de Python bilingüe (Inglés/Español) que se encarga de sincronizar mundos de Minecraft entre una carpeta local y un directorio en la nube. Puede utilizarse a través de su **interfaz gráfica (GUI)**, mediante línea de comandos (CLI) o ejecutarse silenciosamente en segundo plano en la bandeja del sistema (*System Tray*). 

Comprime automáticamente cada mundo en archivos `.zip` en la nube para optimizar la velocidad de subida/bajada. Además, cuenta con mecanismos avanzados de seguridad: escritura atómica, validación de integridad de los ZIP y un sistema de bloqueo (*lock*) para evitar corrupciones si se intenta sincronizar desde varios PCs simultáneamente. Compatible con Windows y Linux.

## Advertencia
Este script utiliza operaciones de compresión, sobrescritura y borrado. Aunque cuenta con validaciones de seguridad, se recomienda encarecidamente **hacer una copia de seguridad manual** de tus mundos antes de usar la herramienta por primera vez, para evitar pérdidas de progreso en caso de configurar las rutas incorrectamente.

## Prerrequisitos
* Python 3.8 o superior.
* **Tener tu servicio de nube instalado localmente** (ej. la aplicación de escritorio de Google Drive, OneDrive, Dropbox, etc.), ya que el programa interactúa con la carpeta de sincronización local que crean estos servicios en tu disco duro.
* **Dependencias de Python:** Instala las librerías necesarias ejecutando:
  ```bash
  pip install psutil PySide6
  ```
  *(Nota para usuarios de Linux con GNOME: asegúrate de tener instalada y habilitada la extensión "AppIndicator and KStatusNotifierItem Support" para poder visualizar el icono nativo en la bandeja del sistema).*

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

## Uso mediante Interfaz Gráfica (GUI)

La forma más sencilla de utilizar el programa es mediante su interfaz visual. Simplemente ejecuta:

```bash
python main.py
```

Esto abrirá una ventana donde podrás:
* **Configurar las rutas** locales y de la nube fácilmente.
* Establecer **parámetros de autoarranque personalizados** y activar/desactivar el inicio automático con el sistema.
* Monitorear el progreso y detectar errores a través de una **consola de registros en tiempo real**.
* Lanzar sincronizaciones manuales con un solo clic.

Al cerrar la ventana (la "X"), el programa no se apagará, sino que se minimizará a la bandeja del sistema (junto al reloj) para seguir realizando sincronizaciones automáticas en segundo plano.

## Uso por Línea de Comandos (CLI)

Si prefieres automatizar tareas o usar la terminal, el programa conserva todos sus argumentos CLI originales:

```text
main.py [-h] [-slp SETLOCALP] [-scp SETCLOUDP] [-dr]
        [-bla BLACKLIST_ADD [BLACKLIST_ADD ...]]
        [-blr BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]] [-l {en,es}]
        [-t] [-d] [-i INTERVAL]
        [{sync}]

positional arguments:
  {sync}                Sincroniza los mundos locales y en la nube y abre la interfaz

options:
  -h, --help            Muestra las opciones del programa
  -slp, --setlocalp SETLOCALP
                        Establece la ruta local de los mundos
  -scp, --setcloudp SETCLOUDP
                        Establece la ruta de la nube de los mundos
  -dr, --dry-run        Realiza una simulación sin modificar archivos
  -bla, --blacklist-add BLACKLIST_ADD [BLACKLIST_ADD ...]
                        Agrega uno o más mundos a la lista negra
  -blr, --blacklist-remove BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]
                        Elimina uno o más mundos de la lista negra
  -l, --lang {en,es}    Establece el idioma (en/es)
  -t, --tray            Inicia el programa directamente oculto en la bandeja del sistema
  -d, --delay           Retrasa el inicio 5 minutos
  -i, --interval INTERVAL
                        Minutos entre cada sincronización automática (por defecto: 30)
```

### Ejemplos de comandos útiles

#### 1. Modo Bandeja del Sistema Oculto (Ideal para el inicio del PC)
Inicia la aplicación de forma invisible (sin abrir la ventana) para sincronizaciones periódicas:
```bash
python main.py --tray
```
*Opcional: Añade `--delay` para esperar 5 minutos antes de la primera comprobación (útil al iniciar sesión para dar tiempo a que tu nube conecte a internet).*

#### 2. Gestión de la Lista Negra (Blacklist)
Si tienes mundos de prueba que no quieres subir a la nube, el programa los ignorará si los añades a la lista negra:
```bash
python main.py -bla "Mundo Pruebas" "Mundo Hardcore"
```
Para quitarlos de la lista negra:
```bash
python main.py -blr "Mundo Pruebas"
```

#### 3. Cambio de Idioma (CLI)
Puedes cambiar la interfaz al español permanentemente con un solo comando:
```bash
python main.py -l es
```

## Mecanismos de Seguridad Incluidos
* **Detección de Minecraft:** El programa utiliza `psutil` para detectar si el juego está abierto y pausa las sincronizaciones automáticas para evitar corromper los archivos de guardado en uso.
* **Escritura Atómica:** Los mundos se comprimen primero en archivos temporales y solo se reemplazan cuando la compresión finaliza con éxito, protegiendo tus datos contra apagones repentinos o cierres forzados.
* **Validación de Integridad:** Antes de sobrescribir tu mundo local, se verifica internamente que el archivo `.zip` de la nube esté completo y contenga los archivos base del juego (`level.dat`), evitando machacar tu mundo con descargas corruptas.
* **Sistema Lock:** Emplea un archivo de bloqueo (`mssync.lock`) en la nube para impedir colisiones catastróficas si dos ordenadores intentan sincronizar modificaciones exactamente al mismo tiempo.