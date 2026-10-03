# Minecraft-Save-Sync

🌍 *Leer en otros idiomas: [English](README.md), [Español](README.es.md).*

---

Aplicación de escritorio y script de Python bilingüe (Inglés/Español) que se encarga de sincronizar mundos de Minecraft entre una carpeta local y un directorio en la nube. Puede utilizarse a través de su **interfaz gráfica (GUI)**, mediante línea de comandos (CLI) o ejecutarse silenciosamente en segundo plano en la bandeja del sistema (*System Tray*). 

Comprime automáticamente cada mundo en archivos `.zip` en la nube para optimizar la velocidad de subida/bajada. Además, cuenta con mecanismos avanzados de seguridad: escritura atómica, validación de integridad de los ZIP y un sistema de bloqueo (*lock*) para evitar corrupciones si se intenta sincronizar desde varios PCs simultáneamente. Compatible con Windows y Linux.

## Advertencia y Uso Obligatorio de la Nube
> [!IMPORTANT]
> **Antes de ejecutar o programar el sincronizador**, es obligatorio que tu cliente de la nube (OneDrive, Google Drive, rclone, etc.) haya terminado de actualizar la carpeta virtual en tu equipo. Si la carpeta de la nube local no está sincronizada con el servidor, esta herramienta no detectará los cambios recientes y no podrá descargar la última versión de tus mundos.

> [!TIP]
> **Recomendación sobre clientes de nube:** Se recomienda encarecidamente utilizar **OneDrive** para la sincronización. El cliente de escritorio de Google Drive es notablemente más lento procesando los cambios locales y tiende a dar más problemas de retrasos o archivos bloqueados.

Este script utiliza operaciones de compresión, sobrescritura y borrado. Aunque cuenta con validaciones de seguridad, se recomienda encarecidamente **hacer una copia de seguridad manual** de tus mundos antes de usar la herramienta por primera vez, para evitar pérdidas de progreso en caso de configurar las rutas incorrectamente.

## Instalación (Método Recomendado)

La forma más rápida y sencilla de usar el programa sin necesidad de instalar Python ni ninguna dependencia es descargar el **ejecutable precompilado**:

1. Ve a la sección de **[Releases](https://github.com/AlejandroSocas/Minecraft-Save-Sync/releases)** en la página del repositorio de GitHub.
2. Descarga el archivo generado para tu sistema operativo (Windows o Linux).
3. Descomprímelo en la carpeta donde desees guardar el programa.
4. Haz doble clic en el ejecutable y la aplicación arrancará inmediatamente.

### Comandos útiles para autostart en GUI
```text
  -t, --tray              Inicia el programa en la bandeja del sistema
  -d, --delay             Retrasa el inicio 5 minutos
  -i, --interval INTERVAL Minutos entre cada sincronización automática
  -b, --block-autosync    Inicia el programa en la bandeja del sistema
```

---

## Ejecución desde el Código Fuente (Para desarrolladores)

Si prefieres ejecutar el script directamente desde Python, sigue estos pasos:

### Prerrequisitos
* Python 3.8 o superior.
* **Tener tu servicio de nube instalado localmente** (ej. la aplicación de escritorio de OneDrive, Google Drive, Dropbox, etc.).
* **Dependencias de Python:** Instala las librerías necesarias ejecutando:
  ```bash
  pip install psutil PySide6
  ```
  *(Nota para usuarios de Linux con GNOME: asegúrate de tener instalada y habilitada la extensión "AppIndicator and KStatusNotifierItem Support" para poder visualizar el icono nativo en la bandeja del sistema).*

### Descarga del código

**Opción A: Usando Git**
```bash
git clone https://github.com/AlejandroSocas/Minecraft-Save-Sync.git
cd Minecraft-Save-Sync
```

**Opción B: Descarga manual**
Haz clic en el botón verde "<> Code" en la parte superior derecha de esta página, selecciona "Download ZIP" y descomprímelo en tu equipo.

---

## Uso mediante Interfaz Gráfica (GUI)

La forma más sencilla de utilizar el programa es mediante su interfaz visual. Simplemente abre el ejecutable (o ejecuta `python main.py`).

Esto abrirá una ventana donde podrás:
* **Configurar las rutas** locales y de la nube fácilmente.
* Establecer **parámetros de autoarranque personalizados** y activar/desactivar el inicio automático con el sistema.
* **Cambiar el idioma (Inglés/Español)** dinámicamente con un selector integrado.
* Monitorear el progreso y detectar errores a través de una **consola de registros en tiempo real**.
* Lanzar sincronizaciones manuales con un solo clic.

Al cerrar la ventana (la "X"), el programa no se apagará, sino que se minimizará a la bandeja del sistema (junto al reloj) para seguir realizando sincronizaciones automáticas en segundo plano.

## Compilación (Crear un Ejecutable local)

*Nota: En la pestaña de **Releases** de GitHub ya tienes disponibles los ejecutables generados automáticamente para Windows y Linux mediante GitHub Actions. Solo necesitas seguir estos pasos si has modificado el código fuente y quieres compilar tu propia versión.*

Puedes compilar el proyecto en un ejecutable independiente usando `PyInstaller`:

1. Instala la herramienta de compilación:
   ```bash
   pip install pyinstaller
   ```
2. Ejecuta el comando de compilación ocultando la consola (`--noconsole`) y añadiendo el icono (`--add-data`):
   * **En Windows:**
     ```bash
     pyinstaller --noconsole --add-data "icono.png;." main.py
     ```
   * **En Linux:**
     ```bash
     pyinstaller --noconsole --add-data "icono.png:." main.py
     ```
3. Una vez termine, encontrarás tu programa compilado y listo para usarse haciendo doble clic dentro de la carpeta `dist`.

*Nota:* El sistema de **autoarranque detectará automáticamente** que el programa está compilado y configurará las rutas del sistema operativo apuntando al ejecutable, por lo que todo funcionará a la perfección.

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
  -b, --block-autosync  Bloquea la función de autosincronización
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

## Comportamientos Importantes a Tener en Cuenta
* **Ubicación de la Configuración:** El archivo de ajustes (`config.json`) se guarda en `%APPDATA%\MSSync` (Windows) o `~/.config/mssync` (Linux). Esto asegura que tu configuración sobreviva al actualizar el ejecutable.
* **Borrado de Mundos:** Borrar un mundo local **no** lo borrará de la nube. La nube actúa como una copia de seguridad eterna. Si deseas eliminar un mundo permanentemente, debes borrarlo tanto en local como en la carpeta de la nube.
* **Conflictos:** Si un mundo ha sido modificado tanto en local como en la nube desde la última sincronización, se produce un conflicto. El mundo local se renombrará a `TuMundo_Conflicto_TIMESTAMP` (se mantendrá en local como copia de seguridad, visible en Minecraft, pero excluido de la sincronización) y se descargará la versión de la nube.

## Mecanismos de Seguridad Incluidos
* **Detección de Minecraft:** El programa utiliza `psutil` para detectar si el juego está abierto y pausa las sincronizaciones automáticas para evitar corromper los archivos de guardado en uso.
* **Escritura Atómica:** 
  * *Subidas:* Los mundos se comprimen directamente en la carpeta de la nube para evitar problemas de reemplazo atómico con las unidades virtuales.
  * *Descargas:* El zip de la nube se copia secuencialmente a local, se extrae en una carpeta temporal segura (`_extraccion_mssync`), y solo reemplaza la carpeta real del mundo cuando la extracción ha finalizado por completo.
* **Validación de Integridad:** Antes de sobrescribir tu mundo local, se verifica internamente que el archivo `.zip` de la nube esté completo y contenga los archivos base del juego (`level.dat`), evitando machacar tu mundo con descargas corruptas.
* **Sistema Lock:** Emplea un archivo de bloqueo (`mssync.lock`) en la nube para impedir colisiones catastróficas si dos ordenadores intentan sincronizar modificaciones exactamente al mismo tiempo.