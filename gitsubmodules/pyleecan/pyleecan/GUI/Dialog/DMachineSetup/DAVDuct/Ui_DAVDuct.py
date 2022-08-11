# -*- coding: utf-8 -*-

# File generated according to DAVDuct.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .....GUI.Tools.HelpButton import HelpButton

from pyleecan.GUI.Resources import pyleecan_rc


class Ui_DAVDuct(object):
    def setupUi(self, DAVDuct):
        if not DAVDuct.objectName():
            DAVDuct.setObjectName("DAVDuct")
        DAVDuct.resize(767, 630)
        icon = QIcon()
        icon.addFile(
            ":/images/images/icon/pyleecan_64.png", QSize(), QIcon.Normal, QIcon.Off
        )
        DAVDuct.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(DAVDuct)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.b_new = QPushButton(DAVDuct)
        self.b_new.setObjectName("b_new")

        self.horizontalLayout_2.addWidget(self.b_new)

        self.b_remove = QPushButton(DAVDuct)
        self.b_remove.setObjectName("b_remove")

        self.horizontalLayout_2.addWidget(self.b_remove)

        self.b_help = HelpButton(DAVDuct)
        self.b_help.setObjectName("b_help")
        self.b_help.setPixmap(QPixmap(":/images/images/icon/help_16.png"))

        self.horizontalLayout_2.addWidget(self.b_help)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tab_vent = QTabWidget(DAVDuct)
        self.tab_vent.setObjectName("tab_vent")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tab_vent.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab_vent.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tab_vent)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalSpacer_5 = QSpacerItem(
            218, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.b_plot = QPushButton(DAVDuct)
        self.b_plot.setObjectName("b_plot")

        self.horizontalLayout_4.addWidget(self.b_plot)

        self.b_cancel = QPushButton(DAVDuct)
        self.b_cancel.setObjectName("b_cancel")

        self.horizontalLayout_4.addWidget(self.b_cancel)

        self.b_ok = QPushButton(DAVDuct)
        self.b_ok.setObjectName("b_ok")

        self.horizontalLayout_4.addWidget(self.b_ok)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(DAVDuct)

        QMetaObject.connectSlotsByName(DAVDuct)

    # setupUi

    def retranslateUi(self, DAVDuct):
        DAVDuct.setWindowTitle(
            QCoreApplication.translate("DAVDuct", "Set axial cooling duct", None)
        )
        self.b_new.setText(QCoreApplication.translate("DAVDuct", "Add New Set", None))
        self.b_remove.setText(
            QCoreApplication.translate("DAVDuct", "Remove Last Set", None)
        )
        self.b_help.setText("")
        self.tab_vent.setTabText(
            self.tab_vent.indexOf(self.tab),
            QCoreApplication.translate("DAVDuct", "Tab 1", None),
        )
        self.tab_vent.setTabText(
            self.tab_vent.indexOf(self.tab_2),
            QCoreApplication.translate("DAVDuct", "Tab 2", None),
        )
        self.b_plot.setText(QCoreApplication.translate("DAVDuct", "Preview", None))
        self.b_cancel.setText(QCoreApplication.translate("DAVDuct", "Cancel", None))
        self.b_ok.setText(QCoreApplication.translate("DAVDuct", "Ok", None))

    # retranslateUi
