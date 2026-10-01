# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ventana.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(608, 457)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.local_path_label = QLabel(self.centralwidget)
        self.local_path_label.setObjectName(u"local_path_label")

        self.gridLayout.addWidget(self.local_path_label, 0, 0, 1, 1)

        self.local_path_line_edit = QLineEdit(self.centralwidget)
        self.local_path_line_edit.setObjectName(u"local_path_line_edit")

        self.gridLayout.addWidget(self.local_path_line_edit, 0, 1, 1, 2)

        self.cloud_path_label = QLabel(self.centralwidget)
        self.cloud_path_label.setObjectName(u"cloud_path_label")

        self.gridLayout.addWidget(self.cloud_path_label, 1, 0, 1, 1)

        self.cloud_path_line_edit = QLineEdit(self.centralwidget)
        self.cloud_path_line_edit.setObjectName(u"cloud_path_line_edit")

        self.gridLayout.addWidget(self.cloud_path_line_edit, 1, 1, 1, 2)

        self.autostart_parameters_label = QLabel(self.centralwidget)
        self.autostart_parameters_label.setObjectName(u"autostart_parameters_label")

        self.gridLayout.addWidget(self.autostart_parameters_label, 2, 0, 1, 2)

        self.autostart_parameters_line_edit = QLineEdit(self.centralwidget)
        self.autostart_parameters_line_edit.setObjectName(u"autostart_parameters_line_edit")

        self.gridLayout.addWidget(self.autostart_parameters_line_edit, 2, 2, 1, 1)

        self.boton_sync = QPushButton(self.centralwidget)
        self.boton_sync.setObjectName(u"boton_sync")

        self.gridLayout.addWidget(self.boton_sync, 3, 0, 1, 3)

        self.consola = QTextEdit(self.centralwidget)
        self.consola.setObjectName(u"consola")

        self.gridLayout.addWidget(self.consola, 4, 0, 1, 3)

        self.setlp = QPushButton(self.centralwidget)
        self.setlp.setObjectName(u"setlp")

        self.gridLayout.addWidget(self.setlp, 0, 3, 1, 1)

        self.setcp = QPushButton(self.centralwidget)
        self.setcp.setObjectName(u"setcp")

        self.gridLayout.addWidget(self.setcp, 1, 3, 1, 1)

        self.autostart_checkbox = QCheckBox(self.centralwidget)
        self.autostart_checkbox.setObjectName(u"autostart_checkbox")

        self.gridLayout.addWidget(self.autostart_checkbox, 3, 3, 1, 1)

        self.SetAP = QPushButton(self.centralwidget)
        self.SetAP.setObjectName(u"SetAP")

        self.gridLayout.addWidget(self.SetAP, 2, 3, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 608, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.local_path_label.setText(QCoreApplication.translate("MainWindow", u"Local Path:", None))
        self.local_path_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"C:\\local_saves_path", None))
        self.cloud_path_label.setText(QCoreApplication.translate("MainWindow", u"Cloud Path:", None))
        self.cloud_path_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"C:\\cloud_saves_path", None))
        self.autostart_parameters_label.setText(QCoreApplication.translate("MainWindow", u"Autostart Parameters:", None))
        self.autostart_parameters_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"-d -i 2 ...", None))
        self.boton_sync.setText(QCoreApplication.translate("MainWindow", u"Sync", None))
        self.setlp.setText(QCoreApplication.translate("MainWindow", u"SetLP", None))
        self.setcp.setText(QCoreApplication.translate("MainWindow", u"SetCP", None))
        self.autostart_checkbox.setText(QCoreApplication.translate("MainWindow", u"Autostart", None))
        self.SetAP.setText(QCoreApplication.translate("MainWindow", u"SetAP", None))
    # retranslateUi

