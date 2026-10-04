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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QGridLayout, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QTimeEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(623, 450)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.consola = QTextEdit(self.centralwidget)
        self.consola.setObjectName(u"consola")

        self.gridLayout.addWidget(self.consola, 5, 0, 1, 3)

        self.autostart_parameters_label = QLabel(self.centralwidget)
        self.autostart_parameters_label.setObjectName(u"autostart_parameters_label")

        self.gridLayout.addWidget(self.autostart_parameters_label, 2, 0, 1, 2)

        self.autostart_checkbox = QCheckBox(self.centralwidget)
        self.autostart_checkbox.setObjectName(u"autostart_checkbox")

        self.gridLayout.addWidget(self.autostart_checkbox, 4, 4, 1, 1)

        self.blacklist_label = QLabel(self.centralwidget)
        self.blacklist_label.setObjectName(u"blacklist_label")

        self.gridLayout.addWidget(self.blacklist_label, 3, 0, 1, 2)

        self.setlp = QPushButton(self.centralwidget)
        self.setlp.setObjectName(u"setlp")

        self.gridLayout.addWidget(self.setlp, 0, 4, 1, 1)

        self.autostart_parameters_line_edit = QLineEdit(self.centralwidget)
        self.autostart_parameters_line_edit.setObjectName(u"autostart_parameters_line_edit")

        self.gridLayout.addWidget(self.autostart_parameters_line_edit, 2, 2, 1, 1)

        self.local_path_label = QLabel(self.centralwidget)
        self.local_path_label.setObjectName(u"local_path_label")

        self.gridLayout.addWidget(self.local_path_label, 0, 0, 1, 1)

        self.local_path_line_edit = QLineEdit(self.centralwidget)
        self.local_path_line_edit.setObjectName(u"local_path_line_edit")

        self.gridLayout.addWidget(self.local_path_line_edit, 0, 1, 1, 2)

        self.setbl = QPushButton(self.centralwidget)
        self.setbl.setObjectName(u"setbl")

        self.gridLayout.addWidget(self.setbl, 3, 4, 1, 1)

        self.cloud_path_line_edit = QLineEdit(self.centralwidget)
        self.cloud_path_line_edit.setObjectName(u"cloud_path_line_edit")

        self.gridLayout.addWidget(self.cloud_path_line_edit, 1, 1, 1, 2)

        self.SetAP = QPushButton(self.centralwidget)
        self.SetAP.setObjectName(u"SetAP")

        self.gridLayout.addWidget(self.SetAP, 2, 4, 1, 1)

        self.cloud_path_label = QLabel(self.centralwidget)
        self.cloud_path_label.setObjectName(u"cloud_path_label")

        self.gridLayout.addWidget(self.cloud_path_label, 1, 0, 1, 1)

        self.boton_sync = QPushButton(self.centralwidget)
        self.boton_sync.setObjectName(u"boton_sync")

        self.gridLayout.addWidget(self.boton_sync, 4, 2, 1, 1)

        self.setcp = QPushButton(self.centralwidget)
        self.setcp.setObjectName(u"setcp")

        self.gridLayout.addWidget(self.setcp, 1, 4, 1, 1)

        self.blacklist_line_edit = QLineEdit(self.centralwidget)
        self.blacklist_line_edit.setObjectName(u"blacklist_line_edit")

        self.gridLayout.addWidget(self.blacklist_line_edit, 3, 2, 1, 1)

        self.select_language = QComboBox(self.centralwidget)
        self.select_language.addItem("")
        self.select_language.addItem("")
        self.select_language.setObjectName(u"select_language")

        self.gridLayout.addWidget(self.select_language, 4, 0, 1, 2)

        self.timeEdit = QTimeEdit(self.centralwidget)
        self.timeEdit.setObjectName(u"timeEdit")
        font = QFont()
        font.setPointSize(16)
        self.timeEdit.setFont(font)
        self.timeEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.gridLayout.addWidget(self.timeEdit, 5, 4, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 623, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.autostart_parameters_label.setText(QCoreApplication.translate("MainWindow", u"Autostart Parameters:", None))
        self.autostart_checkbox.setText(QCoreApplication.translate("MainWindow", u"Autostart", None))
        self.blacklist_label.setText(QCoreApplication.translate("MainWindow", u"Blacklist of Worlds", None))
        self.setlp.setText(QCoreApplication.translate("MainWindow", u"SetLP", None))
        self.autostart_parameters_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"-d -i 2 ...", None))
        self.local_path_label.setText(QCoreApplication.translate("MainWindow", u"Local Path:", None))
        self.local_path_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"C:\\local_saves_path", None))
        self.setbl.setText(QCoreApplication.translate("MainWindow", u"SetBL", None))
        self.cloud_path_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"C:\\cloud_saves_path", None))
        self.SetAP.setText(QCoreApplication.translate("MainWindow", u"SetAP", None))
        self.cloud_path_label.setText(QCoreApplication.translate("MainWindow", u"Cloud Path:", None))
        self.boton_sync.setText(QCoreApplication.translate("MainWindow", u"Sync", None))
        self.setcp.setText(QCoreApplication.translate("MainWindow", u"SetCP", None))
        self.blacklist_line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"world1, world 2, world3", None))
        self.select_language.setItemText(0, QCoreApplication.translate("MainWindow", u"English", None))
        self.select_language.setItemText(1, QCoreApplication.translate("MainWindow", u"Espa\u00f1ol", None))

        self.timeEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"h:mm:ss", None))
    # retranslateUi

