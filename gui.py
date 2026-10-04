from PySide6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QTimer, QTime
from ui_ventana import Ui_MainWindow

from sync_core import *


class Ventana(QMainWindow):
  def __init__(self, args):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.args = args
    self.setWindowTitle("MSSync")
    self.setWindowIcon(QIcon(obtener_ruta_recurso("icono.png")))

    # Hacemos la consola solo se pueda leer
    self.ui.consola.setReadOnly(True)
    self.ui.timeEdit.setReadOnly(True)

    # Estado interno de la sincronización y del cierre
    self.worker = None
    self.saliendo = False

    # Configurar el menú del tray ANTES de traducir
    self.configurar_tray()

    idioma_guardado = "en"
    parametros_guardados = "-d"

    # Precargamos las rutas y parámetros de autoarranque para mostrarlas si existen
    config = leer_config()
    if "ruta_local" in config:
      self.ui.local_path_line_edit.setText(config["ruta_local"])
    if "ruta_nube" in config:
      self.ui.cloud_path_line_edit.setText(config["ruta_nube"])
    if "parametros_autoarranque" in config:
      parametros_guardados = config["parametros_autoarranque"]
    if "idioma" in config:
      idioma_guardado = config["idioma"]
    if "blacklist" in config:
      self.ui.blacklist_line_edit.setText(", ".join(config["blacklist"]))

    if hubo_config_corrupta():
      self.actualizar_consola(t("config_corrupt"))

    self.ui.autostart_parameters_line_edit.setText(parametros_guardados)

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
    self.ui.setbl.clicked.connect(self.establecer_blacklist)

    if self.args.dry_run:
      self.actualizar_consola(t("dry_mode_active"))

    self.timer_tick = QTimer(self)
    self.timer_tick.setInterval(1000)
    self.timer_tick.timeout.connect(self.actualizar_contador_ui)

    self.segundos_restantes = 0
    
    # Validamos el intervalo aquí para poder imprimir los errores en la consola visual
    if self.args.interval:
      try:
        self.args.interval = int(self.args.interval)
        if self.args.interval <= 0:
          self.actualizar_consola(t("interval_range_error").format(self.args.interval))
          self.args.interval = 30
      except ValueError:
        self.actualizar_consola(t("interval_int_error").format(self.args.interval))
        self.args.interval = 30

    if not self.args.block_autosync:
      if self.args.delay:
        # Si hay delay, empezamos la cuenta regresiva de 5 minutos
        self.actualizar_consola(t("delay_start"))
        self.iniciar_cuenta_regresiva(5 * 60, self.iniciar_ciclo_automatico)
      else:
        # Sin delay, iniciamos el ciclo inmediatamente (hará una sync y pondrá el contador a X minutos)
        self.iniciar_ciclo_automatico()
    else:
      self.actualizar_consola(t("block_autosync"))
      
    # Si el autoarranque ya estaba activado, lo regeneramos para que apunte a la ruta de este ejecutable nuevo
    if autoarranque_activado():
      if alternar_autoarranque(True) == False:
        self.actualizar_consola(t("autostart_error"))

    # Forzamos la traducción de la interfaz al terminar de cargar todo
    self.traducir_interfaz()

  def iniciar_cuenta_regresiva(self, segundos, callback_al_terminar):
    """Configura los segundos restantes y la acción a ejecutar al llegar a 0."""
    self.segundos_restantes = segundos
    self.mostrar_tiempo(self.segundos_restantes)
    self.callback_fin_tiempo = callback_al_terminar
    self.timer_tick.start()

  def actualizar_contador_ui(self):
    """Se ejecuta cada 1 segundo para restar y pintar el nuevo valor."""
    if self.segundos_restantes > 0:
      self.segundos_restantes -= 1
      self.mostrar_tiempo(self.segundos_restantes)

    if self.segundos_restantes <= 0:
      self.timer_tick.stop()
      if hasattr(self, "callback_fin_tiempo") and self.callback_fin_tiempo:
        cb = self.callback_fin_tiempo
        self.callback_fin_tiempo = None
        cb()

  def mostrar_tiempo(self, total_segundos):
    """Pinta los segundos en el widget (formato mm:ss)."""
    minutos, segs = divmod(total_segundos, 60)
    horas, minutos = divmod(minutos, 60)

    self.ui.timeEdit.setTime(QTime(horas, minutos, segs))

  def cambiar_idioma(self, index):
    """Se ejecuta cada vez que el usuario cambia el valor del ComboBox"""
    nuevo_idioma = "en" if index == 0 else "es"
    
    # Cambiamos la variable global
    establecer_idioma(nuevo_idioma)
    
    # Guardamos el cambio en config.json
    actualizar_config("idioma", nuevo_idioma)
    
    # Refrescamos todos los textos de la pantalla
    self.traducir_interfaz()
    self.actualizar_consola(t("saving_lang").format(nuevo_idioma))

  def traducir_interfaz(self):
    """Traduce la interfaz según el idioma del programa"""
    self.ui.local_path_label.setText(t("lbl_local"))
    self.ui.cloud_path_label.setText(t("lbl_cloud"))
    self.ui.autostart_parameters_label.setText(t("lbl_autostart"))
    self.ui.boton_sync.setText(t("btn_sync"))
    self.ui.autostart_checkbox.setText(t("chkbx_autostart"))
    self.ui.setlp.setText(t("btn_local"))
    self.ui.setcp.setText(t("btn_cloud"))
    self.ui.SetAP.setText(t("btn_autostart"))
    self.ui.local_path_line_edit.setPlaceholderText(t("placeholder_local"))
    self.ui.cloud_path_line_edit.setPlaceholderText(t("placeholder_cloud"))
    self.ui.blacklist_line_edit.setPlaceholderText(t("placeholder_blacklist"))
    self.ui.setbl.setText(t("btn_blacklist"))
    self.ui.blacklist_label.setText(t("lbl_blacklist"))

    self.accion_abrir.setText(t("tray_open"))
    self.accion_sync.setText(t("tray_sync"))
    self.accion_salir.setText(t("tray_exit"))

  def iniciar_ciclo_automatico(self):
    """Ejecuta la primera sincronización y arranca el ciclo regular"""
    self.empezar_sincronizacion()
    segundos_ciclo = int(self.args.interval * 60)
    self.iniciar_cuenta_regresiva(segundos_ciclo, self.iniciar_ciclo_automatico)

  def empezar_sincronizacion(self):
    """Lanza la sincronización en segundo plano"""
    # Comprobar si Minecraft está en ejecución
    if minecraft_en_ejecucion():
      self.actualizar_consola(t("mc_running"))
      return

    # Comprobar si ya hay una sincronización en curso
    if self.worker is not None and self.worker.isRunning():
      self.actualizar_consola(t("sync_in_progress"))
      return

    self.ui.boton_sync.setEnabled(False)
    self.worker = SyncWorker(args=self.args)
    self.worker.signals.log_message.connect(self.actualizar_consola)
    self.worker.signals.finished.connect(self.sincronizacion_finalizada)
    self.worker.start()

  def actualizar_consola(self, mensaje):
    """Actualiza la consola de la ventana con un mensaje"""
    self.ui.consola.append(mensaje) # Añade texto a la consola virtual

  def sincronizacion_finalizada(self, _):
    """Desbloquea la sincronización una vez finaliza el proceso"""
    if getattr(self, 'saliendo', False):
      QApplication.instance().quit()
    else:
      self.ui.boton_sync.setEnabled(True)

  def asignar_ruta_local(self):
    """Guarda la ruta local introducida en config.json"""
    local_path = validar_ruta(self.ui.local_path_line_edit.text())
    if local_path:
      self.actualizar_consola(t("saving_local").format(local_path))
      actualizar_config("ruta_local", local_path)
    else:
      self.actualizar_consola(t("error_local"))

  def asignar_ruta_nube(self):
    """Guarda la ruta nube introducida en config.json"""
    cloud_path = validar_ruta(self.ui.cloud_path_line_edit.text())
    if cloud_path:
      self.actualizar_consola(t("saving_cloud").format(cloud_path))
      actualizar_config("ruta_nube", cloud_path)
    else:
      self.actualizar_consola(t("error_cloud"))

  def asignar_parametros_autoarranque(self):
    """Guarda los parámetros de autoarranque establecidos en config.json"""
    parametros_autoarranque = self.ui.autostart_parameters_line_edit.text()
    self.actualizar_consola(t("saving_start_parameters").format(parametros_autoarranque))
    actualizar_config("parametros_autoarranque", parametros_autoarranque)
    if autoarranque_activado():
      if alternar_autoarranque(True) == False:
         self.actualizar_consola(t("autostart_error"))
      else:
        self.actualizar_consola(t("auto_updated"))


  def cambiar_autoarranque(self, activado):
    """Cambia el autoarranque a activado o desactivado"""
    if activado:
      if alternar_autoarranque(True):
        self.actualizar_consola(t("auto_enabled"))
      else:
        self.actualizar_consola(t("autostart_error"))
        self.ui.autostart_checkbox.setChecked(False) # Desmarcamos la casilla visualmente porque falló
    else:
      alternar_autoarranque(False)
      self.actualizar_consola(t("auto_disabled"))

  def configurar_tray(self):
    """Configura el menú tray guardaddo en la bandeja del sistema"""
    self.tray_icon = QSystemTrayIcon(QIcon(obtener_ruta_recurso("icono.png")), self)
    self.tray_menu = QMenu()

    # Guardamos las acciones como variables de clase (self.) para poder traducirlas luego
    self.accion_abrir = QAction("", self)
    self.accion_abrir.triggered.connect(self.showNormal)

    self.accion_sync = QAction("", self)
    self.accion_sync.triggered.connect(self.empezar_sincronizacion)

    self.accion_salir = QAction("", self)
    self.accion_salir.triggered.connect(self.salir) 

    self.tray_menu.addAction(self.accion_abrir)
    self.tray_menu.addAction(self.accion_sync)
    self.tray_menu.addSeparator()
    self.tray_menu.addAction(self.accion_salir)

    self.tray_icon.setContextMenu(self.tray_menu)
    self.tray_icon.show()

  def establecer_blacklist(self):
    """Establece la blacklist según lo añadido por el usuario"""
    texto = self.ui.blacklist_line_edit.text()
    # Separamos por comas, quitamos espacios en blanco de los extremos y descartamos vacíos
    elementos = [m.strip() for m in texto.split(",") if m.strip()]
    
    # Eliminamos duplicados que el usuario haya escrito en la misma caja
    nuevos_mundos = []
    for mundo in elementos:
      if mundo not in nuevos_mundos:
        nuevos_mundos.append(mundo)
      else:
        self.actualizar_consola(t("bl_already").format(mundo))
    
    # Leemos la configuración actual usando thread-safe
    datos = leer_config()
    antigua_blacklist = datos.get("blacklist", [])
    
    # Avisamos de los mundos que son nuevos respecto al archivo
    for mundo in nuevos_mundos:
      if mundo not in antigua_blacklist:
        self.actualizar_consola(t("bl_added").format(mundo))
        
    # Avisamos de los mundos que se han eliminado de la lista
    for mundo in antigua_blacklist:
      if mundo not in nuevos_mundos:
        self.actualizar_consola(t("bl_removed").format(mundo))
        
    # Guardamos la lista limpia y sin mundos duplicados
    actualizar_config("blacklist", nuevos_mundos)
    
    # Reescribimos el texto en la caja bien formateado ("Mundo 1, Mundo 2")
    self.ui.blacklist_line_edit.setText(", ".join(nuevos_mundos))

  def salir(self):
    """Sale del programa de forma segura"""
    if self.worker is not None and self.worker.isRunning():
      self.saliendo = True
      self.ui.boton_sync.setEnabled(False)
      self.actualizar_consola(t("exit_waiting"))
      # El QApplication.quit() se llamará en sincronizacion_finalizada
    else:
      QApplication.instance().quit()


  def closeEvent(self, event):
    # Ignoramos la orden de destrucción
    event.ignore()
    # Ocultamos la ventana (desaparece de la barra de tareas normal)
    self.hide()
