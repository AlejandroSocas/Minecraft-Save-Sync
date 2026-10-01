from PySide6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from ui_ventana import Ui_MainWindow

from sync_core import *


class Ventana(QMainWindow):
  def __init__(self, args):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.args = args
    self.setWindowTitle("MSSync")

    if ARCHIVO_CONFIG.exists():
      with open(ARCHIVO_CONFIG, "r") as archivo:
        config = json.load(archivo)
        if "ruta_local" in config:
          self.ui.local_path_line_edit.setText(config["ruta_local"])
        if "ruta_nube" in config:
          self.ui.cloud_path_line_edit.setText(config["ruta_nube"])
        if "parametros_autoarranque" in config:
          self.ui.autostart_parameters_line_edit.setText(config["parametros_autoarranque"])

    self.configurar_tray()

    self.ui.setlp.clicked.connect(self.asignar_ruta_local)
    self.ui.setcp.clicked.connect(self.asignar_ruta_nube)
    self.ui.SetAP.clicked.connect(self.asignar_parametros_autoarranque)
    self.ui.boton_sync.clicked.connect(self.empezar_sincronizacion)
    self.ui.autostart_checkbox.setChecked(autoarranque_activado())
    self.ui.autostart_checkbox.toggled.connect(self.cambiar_autoarranque)

  def empezar_sincronizacion(self):
    self.ui.boton_sync.setEnabled(False) # Bloquear botón para evitar dobles clics
    
    self.worker = SyncWorker(args=self.args)
    # Conectamos las señales a funciones de la GUI
    self.worker.signals.log_message.connect(self.actualizar_consola)
    self.worker.signals.finished.connect(self.sync_finished)
    
    self.worker.start() # Esto llama a run() en segundo plano

  def actualizar_consola(self, mensaje):
    self.ui.consola.append(mensaje) # Añade texto a la consola virtual

  def sincronizacion_finalizada(self, correcto):
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
    # Crear el objeto System Tray y asignarle una imagen
    self.tray_icon = QSystemTrayIcon(QIcon("icono.png"), self)

    # 2. Crear el menú desplegable que saldrá al hacer clic derecho
    self.tray_menu = QMenu()

    # 3. Crear las acciones (los botones) del menú y conectarlas a tus funciones
    accion_abrir = QAction("Abrir interfaz", self)
    accion_abrir.triggered.connect(self.showNormal) # showNormal restaura la ventana

    accion_sync = QAction("Sincronizar ahora", self)
    accion_sync.triggered.connect(self.start_sync)

    accion_salir = QAction("Salir", self)
    # QApplication.instance().quit mata todo el programa de forma segura
    accion_salir.triggered.connect(QApplication.instance().quit) 

    # 4. Añadir las acciones al menú en orden
    self.tray_menu.addAction(accion_abrir)
    self.tray_menu.addAction(accion_sync)
    self.tray_menu.addSeparator() # Pone una línea divisoria estética
    self.tray_menu.addAction(accion_salir)

    # 5. Acoplar el menú al icono y mostrarlo en la barra de tareas
    self.tray_icon.setContextMenu(self.tray_menu)
    self.tray_icon.show()

if __name__ == "__main__":
  app = QApplication(sys.argv)
  ventana = Ventana(args="hola")
  ventana.show()
  sys.exit(app.exec())