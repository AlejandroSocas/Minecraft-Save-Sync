# Minecraft-Save-Sync

🌍 *Read this in other languages: [English](README.md), [Español](README.es.md).*

---

A bilingual (English/Spanish) Python desktop application and script that synchronizes Minecraft worlds between a local folder and a cloud directory. It can be used via its **Graphical User Interface (GUI)**, command-line interface (CLI), or run silently in the background in the system tray.

It automatically compresses each world into `.zip` files in the cloud to optimize upload/download speeds. Additionally, it features advanced security mechanisms: atomic writes, ZIP integrity validation, and a lock system to prevent corruption if synchronization is attempted from multiple PCs simultaneously. Compatible with Windows and Linux.

## Warning
This script uses compression, overwrite, and deletion operations. Although it includes security validations, it is highly recommended to **make a manual backup** of your worlds before using the tool for the first time to avoid any loss of progress in case of an incorrect path configuration.

## Prerequisites
* Python 3.8 or higher.
* **A cloud service installed locally** (e.g., Google Drive, OneDrive, Dropbox desktop app, etc.), as the program interacts with the local sync folder created by these services on your hard drive.
* **Python dependencies:** Install the required libraries by running:
  ~~~bash
  pip install psutil PySide6
  ~~~
  *(Note for Linux GNOME users: make sure to have the "AppIndicator and KStatusNotifierItem Support" extension installed and enabled to view the native icon in the system tray).*

## Installation

You have two options to download and set up the tool on your machine:

**Option A: Using Git (Recommended)**
1. Open your terminal and clone the repository:
   ~~~bash
   git clone https://github.com/AlejandroSocas/Minecraft-Save-Sync.git
   ~~~

2. Navigate to the newly downloaded folder:
   ~~~bash
   cd Minecraft-Save-Sync
   ~~~

**Option B: Manual Download (Without Git)**
1. Click the green "<> Code" button at the top right of this page and select "Download ZIP".
2. Unzip the downloaded file into the folder where you want to save the program.
3. Open a terminal and navigate to that folder (e.g., `cd Downloads/Minecraft-Save-Sync`).

## Graphical User Interface (GUI) Usage

The easiest way to use the program is through its visual interface. Simply run:

~~~bash
python main.py
~~~

This will open a window where you can:
* **Configure the local and cloud paths** easily.
* Set **custom autostart parameters** and enable/disable automatic startup with the system.
* Monitor progress and detect errors through a **real-time log console**.
* Launch manual synchronizations with a single click.

Closing the window (the "X") will not terminate the program; instead, it will minimize it to the system tray (next to the clock) to continue performing automatic synchronizations in the background.

## Command Line (CLI) Usage

If you prefer to automate tasks or use the terminal, the program retains all its original CLI arguments:

~~~text
main.py [-h] [-slp SETLOCALP] [-scp SETCLOUDP] [-dr]
        [-bla BLACKLIST_ADD [BLACKLIST_ADD ...]]
        [-blr BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]] [-l {en,es}]
        [-t] [-d] [-i INTERVAL]
        [{sync}]

positional arguments:
  {sync}                Synchronizes local and cloud worlds and opens the interface

options:
  -h, --help            Shows the program options
  -slp, --setlocalp SETLOCALP
                        Sets the local path for the worlds
  -scp, --setcloudp SETCLOUDP
                        Sets the cloud path for the worlds
  -dr, --dry-run        Performs a simulation without modifying files
  -bla, --blacklist-add BLACKLIST_ADD [BLACKLIST_ADD ...]
                        Adds one or more worlds to the blacklist
  -blr, --blacklist-remove BLACKLIST_REMOVE [BLACKLIST_REMOVE ...]
                        Removes one or more worlds from the blacklist
  -l, --lang {en,es}    Sets the language (en/es)
  -t, --tray            Starts the program directly hidden in the system tray
  -d, --delay           Delays the start by 5 minutes
  -i, --interval INTERVAL
                        Minutes between each automatic synchronization (default: 30)
~~~

### Useful Command Examples

#### 1. Hidden System Tray Mode (Ideal for PC startup)
Starts the application invisibly (without opening the window) for periodic synchronizations:
~~~bash
python main.py --tray
~~~
*Optional: Add `--delay` to wait 5 minutes before the first check (useful upon login to give your cloud service time to connect to the internet).*

#### 2. Blacklist Management
If you have test worlds that you do not want to upload to the cloud, the program will ignore them if you add them to the blacklist:
~~~bash
python main.py -bla "Test World" "Hardcore World"
~~~
To remove them from the blacklist:
~~~bash
python main.py -blr "Test World"
~~~

#### 3. Language Change (CLI)
You can permanently change the interface to Spanish (or English) with a single command:
~~~bash
python main.py -l es
~~~

## Included Security Mechanisms
* **Minecraft Detection:** The program uses `psutil` to detect if the game is open and pauses automatic synchronizations to avoid corrupting save files in use.
* **Atomic Writes:** Worlds are first compressed into temporary files and are only replaced when compression finishes successfully, protecting your data against sudden power outages or forced closures.
* **Integrity Validation:** Before overwriting your local world, it internally verifies that the cloud `.zip` file is complete and contains the base game files (`level.dat`), preventing your world from being overwritten with corrupt downloads.
* **Lock System:** Uses a lock file (`mssync.lock`) in the cloud to prevent catastrophic collisions if two computers attempt to synchronize modifications at the exact same time.