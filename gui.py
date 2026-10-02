from PySide6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QTimer
from ui_ventana import Ui_MainWindow

from sync_core import *


class Ventana(QMainWindow):
  def __init__(self, args):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.args = args
    self.setWindowTitle("MSSync")

    # Hacemos la consola solo se pueda leer
    self.ui.consola.setReadOnly(True)

    # Configurar el menú del tray ANTES de traducir
    self.configurar_tray()

    idioma_guardado = "en"

    # Precargamos las rutas y parámetros de autoarranque para mostrarlas si existen
    if ARCHIVO_CONFIG.exists():
      with open(ARCHIVO_CONFIG, "r") as archivo:
        config = json.load(archivo)
        if "ruta_local" in config:
          self.ui.local_path_line_edit.setText(config["ruta_local"])
        if "ruta_nube" in config:
          self.ui.cloud_path_line_edit.setText(config["ruta_nube"])
        if "parametros_autoarranque" in config:
          self.ui.autostart_parameters_line_edit.setText(config["parametros_autoarranque"])
        if "idioma" in config:
          idioma_guardado = config["idioma"]

    # Configurar el selector de idioma bloqueando las señales temporales
    self.ui.select_language.blockSignals(True)
    if idioma_guardado == "es":
      self.ui.select_language.setCurrentIndex(1) # Selecciona Español
    else:
      self.ui.select_language.setCurrentIndex(0) # Selecciona English
    self.ui.select_language.blockSignals(False)
      
    # Conectamos el cambio del desplegable a nuestra función
    self.ui.select_language.currentIndexChanged.connect(self.cambiar_idioma)

    self.ui.setlp.clicked.connect(self.asignar_ruta_local)
    self.ui.setcp.clicked.connect(self.asignar_ruta_nube)
    self.ui.SetAP.clicked.connect(self.asignar_parametros_autoarranque)
    self.ui.boton_sync.clicked.connect(self.empezar_sincronizacion)
    self.ui.autostart_checkbox.setChecked(autoarranque_activado())
    self.ui.autostart_checkbox.toggled.connect(self.cambiar_autoarranque)

    self.timer_sync = QTimer(self)
    self.timer_sync.timeout.connect(self.empezar_sincronizacion)
    self.timer_sync.start(self.args.interval * 60 * 1000)

    # Forzamos la traducción de la interfaz al terminar de cargar todo
    self.traducir_interfaz()

  def cambiar_idioma(self, index):
    """Se ejecuta cada vez que el usuario cambia el valor del ComboBox"""
    nuevo_idioma = "en" if index == 0 else "es"
    
    # Cambiamos la variable global
    establecer_idioma(nuevo_idioma)
    
    # Guardamos el cambio en config.json
    self.actualizar_config("idioma", nuevo_idioma)
    
    # Refrescamos todos los textos de la pantalla
    self.traducir_interfaz()
    self.actualizar_consola(t("saving_lang").format(nuevo_idioma))

  def traducir_interfaz(self):
    self.ui.local_path_label.setText(t("lbl_local"))
    self.ui.cloud_path_label.setText(t("lbl_cloud"))
    self.ui.autostart_parameters_label.setText(t("lbl_autostart"))
    self.ui.boton_sync.setText(t("btn_sync"))
    self.ui.autostart_checkbox.setText(t("chkbx_autostart"))
    self.ui.setlp.setText(t("btn_local"))
    self.ui.setcp.setText(t("btn_cloud"))
    self.ui.SetAP.setText(t("btn_autostart"))

    self.accion_abrir.setText(t("tray_open"))
    self.accion_sync.setText(t("tray_sync"))
    self.accion_salir.setText(t("tray_exit"))

  def empezar_sincronizacion(self):
    # Comprobar si Minecraft está en ejecución
    if minecraft_en_ejecucion():
      self.actualizar_consola(t("mc_running"))
      return

    # Comprobar si ya hay una sincronización en curso
    if hasattr(self, 'worker') and self.worker.isRunning():
      self.actualizar_consola(t("sync_in_progress"))
      return

    self.ui.boton_sync.setEnabled(False)
    self.worker = SyncWorker(args=self.args)
    self.worker.signals.log_message.connect(self.actualizar_consola)
    self.worker.signals.finished.connect(self.sincronizacion_finalizada)
    self.worker.start()

  def actualizar_consola(self, mensaje):
    self.ui.consola.append(mensaje) # Añade texto a la consola virtual

  def sincronizacion_finalizada(self, _):
    self.ui.boton_sync.setEnabled(True)

  def actualizar_config(self, clave, valor):
    datos = {}
    if ARCHIVO_CONFIG.exists():
      with open(ARCHIVO_CONFIG, "r") as archivo:
        datos = json.load(archivo)

    datos[clave] = valor
    with open(ARCHIVO_CONFIG, "w") as archivo:
      json.dump(datos, archivo, indent=2)

  def asignar_ruta_local(self):
    local_path = self.ui.local_path_line_edit.text()
    self.actualizar_consola(t("saving_local").format(local_path))
    self.actualizar_config("ruta_local", local_path)

  def asignar_ruta_nube(self):
    cloud_path = self.ui.cloud_path_line_edit.text()
    self.actualizar_consola(t("saving_cloud").format(cloud_path))
    self.actualizar_config("ruta_nube", cloud_path)

  def asignar_parametros_autoarranque(self):
    parametros_autoarranque = self.ui.autostart_parameters_line_edit.text()
    self.actualizar_consola(t("saving_start_parameters").format(parametros_autoarranque))
    self.actualizar_config("parametros_autoarranque", parametros_autoarranque)

  def cambiar_autoarranque(self, activado):
    # activado es True si se acaba de marcar, False si se desmarcó
    alternar_autoarranque(activado)
    if activado:
      self.actualizar_consola("Autoarranque activado en el sistema.")
    else:
      self.actualizar_consola("Autoarranque desactivado.")

  def configurar_tray(self):
    self.tray_icon = QSystemTrayIcon(QIcon("icono.png"), self)
    self.tray_menu = QMenu()

    # Guardamos las acciones como variables de clase (self.) para poder traducirlas luego
    self.accion_abrir = QAction("", self)
    self.accion_abrir.triggered.connect(self.showNormal)

    self.accion_sync = QAction("", self)
    self.accion_sync.triggered.connect(self.empezar_sincronizacion)

    self.accion_salir = QAction("", self)
    self.accion_salir.triggered.connect(QApplication.instance().quit) 

    self.tray_menu.addAction(self.accion_abrir)
    self.tray_menu.addAction(self.accion_sync)
    self.tray_menu.addSeparator()
    self.tray_menu.addAction(self.accion_salir)

    self.tray_icon.setContextMenu(self.tray_menu)
    self.tray_icon.show()

  def closeEvent(self, event):
    # Ignoramos la orden de destrucción
    event.ignore()
    # Ocultamos la ventana (desaparece de la barra de tareas normal)
    self.hide()
