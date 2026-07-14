# Minecraft-Save-Sync

🌍 *Read this in other languages: [English](README.md), [Español](README.es.md).*

---

A bilingual (English/Spanish) Python CLI script that synchronizes Minecraft worlds between a local folder and a cloud directory. It is theoretically compatible with Linux, Windows, and macOS, although currently it has only been extensively tested in Linux environments.

## Warning
This script uses overwrite and deletion operations (`shutil`). It is highly recommended to **make a manual backup** of your saves before using the tool for the first time to avoid any loss of progress in case of an incorrect path configuration.

## Prerequisites
This program exclusively uses standard Python libraries, so no external dependencies are required. You only need:
* Python 3.6 or higher.
* **A cloud service installed locally** (e.g., the OneDrive, Google Drive, or Dropbox desktop app), as the script works by interacting with the local sync folder created by these services on your hard drive.

## Installation

You have two options to download and set up the tool on your machine:

**Option A: Using Git (Recommended)**
1. Open your terminal and clone the repository:
   ```bash
   git clone [https://github.com/AlejandroSocas/Minecraft-Save-Sync.git](https://github.com/AlejandroSocas/Minecraft-Save-Sync.git)
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
mssync.py [-h] [-slp SETLOCALP] [-scp SETCLOUDP] [-dr] [-bla BLACKLIST_ADD [BLACKLIST_ADD ...]] [-blr BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]] [-l {en,es}] [{sync}]

positional arguments:
  {sync}                Synchronizes local and cloud worlds

options:
  -h, --help            Shows the program options
  -slp, --setlocalp SETLOCALP
                        Sets the local path for your worlds
  -scp, --setcloudp SETCLOUDP
                        Sets the cloud path for your worlds
  -dr, --dry-run        Performs a simulation of the synchronization without modifying any files
  -bla, --blacklist-add BLACKLIST_ADD [BLACKLIST_ADD ...]
                        Adds one or more worlds to the blacklist
  -blr, --blacklist-remove BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]
                        Removes one or more worlds from the blacklist
  -l, --lang {en,es}    Sets the language (en/es)
```

## Usage Examples

### 1. Initial Configuration
Set the paths for your worlds. This is **only done the first time** and gets saved in `config.json`.
```bash
python mssync.py --setlocalp /home/user/.minecraft/saves/ --setcloudp /home/user/Onedrive/MCSaves/
```

### 2. Synchronization
Run this command every time you finish playing a world to update the cloud.
```bash
python mssync.py sync
```

### 3. Simulation (Dry Run)
If you want to check which worlds would be uploaded, downloaded, or overwritten without making any actual changes to your files, add the `-dr` parameter.
```bash
python mssync.py sync -dr
```

### 4. Blacklist Management
If you have heavy test worlds that you do not want to sync with the cloud, you can add them to the blacklist. The program will automatically and permanently ignore them during every sync until you remove them from the list.

Add worlds:
```bash
python mssync.py -bla "Test World" "Hardcore World"
```

Remove worlds:
```bash
python mssync.py -blr "Test World"
```

### 5. Change Language
The program runs in English by default. You can permanently switch the interface to Spanish with a single command:
```bash
python mssync.py -l es
```

## Prism Launcher Automation (Optional)

You can configure Prism Launcher to automatically sync your worlds every time you close the game, opening a terminal so you can see the process.

1. Right-click your Minecraft instance and select **Edit**.
2. Go to **Settings > Custom Commands**.
3. Check the box to enable custom commands.
4. In the **Post-launch command** field, paste the corresponding command for your operating system:

**Windows:**
`cmd /c start cmd /k "python C:\path\to\mssync.py sync"`

**Linux (GNOME):**
`gnome-terminal -- bash -c "python /path/to/mssync.py sync; echo ''; read -p 'Press Enter to close...'"`

**Linux (KDE):**
`konsole -e bash -c "python /path/to/mssync.py sync; echo ''; read -p 'Press Enter to close...'"`

***Remember to replace "path/to" with the actual absolute path where you installed the program!***