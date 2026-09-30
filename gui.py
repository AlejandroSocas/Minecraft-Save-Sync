# 3. Cómo lo recibe la GUI (gui.py)
class MainWindow(QWidget): # O la clase que generes con Qt Designer
  def start_sync(self):
    self.btn_sync.setEnabled(False) # Bloquear botón para evitar dobles clics
    
    self.worker = SyncWorker(args=self.args)
    # Conectamos las señales a funciones de la GUI
    self.worker.signals.log_message.connect(self.update_log_screen)
    self.worker.signals.finished.connect(self.sync_finished)
    
    self.worker.start() # Esto llama a run() en segundo plano

  def update_log_screen(self, message):
    self.text_edit_logs.append(message) # Añade texto a la consola virtual

  def sync_finished(self, success):
    self.btn_sync.setEnabled(True)