# Minecraft-Save-Sync

🌍 *Read this in other languages: [English](README.md), [Español](README.es.md).*

---

A bilingual (English/Spanish) Python script that synchronizes Minecraft worlds between a local folder and a cloud directory. It can be used via the command-line interface (CLI) or run in the background in the system tray. It automatically compresses worlds into `.zip` archives in the cloud to optimize upload/download speeds and ensure data integrity. Compatible with Windows and Linux.

## Warning
This script uses compression, overwrite, and deletion operations (`shutil`). It is highly recommended to **make a manual backup** of your saves before using the tool for the first time to avoid any loss of progress in case of an incorrect path configuration.

## Prerequisites
* Python 3.6 or higher.
* **A cloud service installed locally** (e.g., Google Drive, OneDrive, or Dropbox desktop app), as the script interacts with the local sync folder created by these services on your hard drive.
* **Python dependencies:** Install the required packages by running:
  ```bash
  pip install psutil pystray Pillow
  ```
  *(Note for Linux GNOME users: ensure the "AppIndicator and KStatusNotifierItem Support" extension is installed and enabled to display system tray icons).*

## Installation

You have two options to download and set up the tool on your machine:

**Option A: Using Git (Recommended)**
1. Open your terminal and clone the repository:
   ```bash
   git clone https://github.com/AlejandroSocas/Minecraft-Save-Sync.git
   ```

2. Navigate to the newly downloaded folder:
   ```bash
   cd Minecraft-Save-Sync
   ```

**Option B: Manual Download (No Git)**
1. Click the green "<> Code" button at the top right of this page and select "Download ZIP".
2. Extract the downloaded file into your desired folder.
3. Open a terminal and navigate to that folder (e.g., `cd Downloads/Minecraft-Save-Sync`).

## General Usage

In your operating system's terminal, inside the folder where you installed the program:

```text
mssync.py [-h] [-slp SETLOCALP] [-scp SETCLOUDP] [-dr]
          [-bla BLACKLIST_ADD [BLACKLIST_ADD ...]]
          [-blr BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]] [-l {en,es}]
          [-t] [-d] [-i INTERVAL]
          [{sync}]

positional arguments:
  {sync}                Synchronizes local and cloud worlds

options:
  -h, --help            Shows the program options
  -slp, --setlocalp SETLOCALP
                        Sets the local path for the worlds
  -scp, --setcloudp SETCLOUDP
                        Sets the cloud path for the worlds
  -dr, --dry-run        Performs a simulation of the synchronization without modifying files
  -bla, --blacklist-add BLACKLIST_ADD [BLACKLIST_ADD ...]
                        Adds one or more worlds to the blacklist
  -blr, --blacklist-remove BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]
                        Removes one or more worlds from the blacklist
  -l, --lang {en,es}    Sets the language (en/es)
  -t, --tray            Starts the program in the system tray
  -d, --delay           Delays the start by 5 minutes
  -i, --interval INTERVAL
                        Minutes between each automatic synchronization (default: 30)
```

## Usage Examples

### 1. Initial Configuration
Set the paths for your worlds. This is **only done the first time** on each computer and gets saved in `config.json`.
```bash
python mssync.py --setlocalp "C:\Users\your_user\AppData\Roaming\.minecraft\saves" --setcloudp "C:\Users\your_user\OneDrive\MCSaves"
```

### 2. System Tray Mode (Background)
Start the resident application next to your operating system's clock for periodic automatic synchronizations:
```bash
python mssync.py --tray
```

Additional options for tray mode:
* **Change the check interval** (e.g., every 15 minutes instead of the default 30):
  ```bash
  python mssync.py --tray -i 15
  ```
* **5-minute startup delay** (ideal on system boot to give your cloud app time to connect to the internet):
  ```bash
  python mssync.py --tray --delay
  ```

**Context menu options (right-click on the tray icon):**
* **Synchronize now:** Forces an immediate check and synchronization.
* **Autostart:** Interactive toggle checkbox to enable or disable automatic launch on system boot (creates a `.bat` in Windows Startup or a `.desktop` in Linux autostart).
* **Exit:** Stops the synchronization thread and closes the tray cleanly.
* *Safety note:* The program automatically detects if Minecraft is currently running via `psutil` and will postpone any synchronization until the game is closed to prevent save corruption.

### 3. Manual CLI Synchronization
If you prefer not to use the tray and want to trigger a one-off sync manually:
```bash
python mssync.py sync
```

### 4. Simulation (Dry Run)
If you want to check which worlds would be uploaded, downloaded, or overwritten without making any actual changes to your files, add the `-dr` parameter.
```bash
python mssync.py sync -dr
```

### 5. Blacklist Management
If you have heavy test worlds that you do not want to sync with the cloud, you can add them to the blacklist. The program will automatically and permanently ignore them during every sync until you remove them from the list.

Add worlds:
```bash
python mssync.py -bla "Test World" "Hardcore World"
```

Remove worlds:
```bash
python mssync.py -blr "Test World"
```

### 6. Change Language
The program runs in English by default. You can permanently switch the interface to Spanish with a single command:
```bash
python mssync.py -l es
```

## Prism Launcher Automation (Optional)

If you prefer not having a background tray app running, you can configure Prism Launcher to automatically sync upon launching and closing the game:

1. Right-click your Minecraft instance and select **Edit**.
2. Go to **Settings > Custom Commands** and check the box to enable custom commands.
3. To download the latest saves before playing, in **Pre-launch command**:
   * **Windows:** `cmd /c "python C:\path\to\mssync.py sync"`
   * **Linux:** `bash -c "python /path/to/mssync.py sync"`
4. To upload modified saves upon exiting, in **Post-exit command**:
   * **Windows:** `cmd /c start cmd /k "python C:\path\to\mssync.py sync"`
   * **Linux (GNOME):** `gnome-terminal -- bash -c "python /path/to/mssync.py sync; echo ''; read -p 'Press Enter to close...'"`
   * **Linux (KDE):** `konsole -e bash -c "python /path/to/mssync.py sync; echo ''; read -p 'Press Enter to close...'"`

***Remember to replace "path/to" with the actual absolute path where you installed the program!***