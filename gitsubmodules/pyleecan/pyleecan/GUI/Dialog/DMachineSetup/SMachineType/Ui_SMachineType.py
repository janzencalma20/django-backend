# -*- coding: utf-8 -*-

# File generated according to SMachineType.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyleecan.GUI.Resources import pyleecan_rc


class Ui_SMachineType(object):
    def setupUi(self, SMachineType):
        if not SMachineType.objectName():
            SMachineType.setObjectName("SMachineType")
        SMachineType.resize(650, 550)
        SMachineType.setMinimumSize(QSize(650, 550))
        self.verticalLayout = QVBoxLayout(SMachineType)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.in_machine_type = QLabel(SMachineType)
        self.in_machine_type.setObjectName("in_machine_type")

        self.horizontalLayout_5.addWidget(self.in_machine_type)

        self.c_type = QComboBox(SMachineType)
        self.c_type.addItem("")
        self.c_type.addItem("")
        self.c_type.addItem("")
        self.c_type.addItem("")
        self.c_type.addItem("")
        self.c_type.addItem("")
        self.c_type.addItem("")
        self.c_type.setObjectName("c_type")

        self.horizontalLayout_5.addWidget(self.c_type)

        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.img_type_machine = QLabel(SMachineType)
        self.img_type_machine.setObjectName("img_type_machine")
        self.img_type_machine.setMinimumSize(QSize(300, 300))
        self.img_type_machine.setMaximumSize(QSize(400, 400))
        self.img_type_machine.setPixmap(
            QPixmap(":/images/images/MachineSetup/MachineType/machine_SCIM.png")
        )
        self.img_type_machine.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.img_type_machine)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.txt_type_machine = QTextEdit(SMachineType)
        self.txt_type_machine.setObjectName("txt_type_machine")
        self.txt_type_machine.setMaximumSize(QSize(16777215, 30))
        self.txt_type_machine.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse
        )

        self.verticalLayout.addWidget(self.txt_type_machine)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.is_inner_rotor = QCheckBox(SMachineType)
        self.is_inner_rotor.setObjectName("is_inner_rotor")
        self.is_inner_rotor.setChecked(True)

        self.horizontalLayout.addWidget(self.is_inner_rotor)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.in_name = QLabel(SMachineType)
        self.in_name.setObjectName("in_name")

        self.horizontalLayout.addWidget(self.in_name)

        self.le_name = QLineEdit(SMachineType)
        self.le_name.setObjectName("le_name")
        self.le_name.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.le_name)

        self.horizontalSpacer_5 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.in_p = QLabel(SMachineType)
        self.in_p.setObjectName("in_p")

        self.horizontalLayout.addWidget(self.in_p)

        self.si_p = QSpinBox(SMachineType)
        self.si_p.setObjectName("si_p")
        self.si_p.setMinimum(1)
        self.si_p.setMaximum(999999)
        self.si_p.setValue(1)

        self.horizontalLayout.addWidget(self.si_p)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.b_previous = QPushButton(SMachineType)
        self.b_previous.setObjectName("b_previous")
        self.b_previous.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.b_previous)

        self.b_next = QPushButton(SMachineType)
        self.b_next.setObjectName("b_next")

        self.horizontalLayout_2.addWidget(self.b_next)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.si_p, self.b_next)

        self.retranslateUi(SMachineType)

        QMetaObject.connectSlotsByName(SMachineType)

    # setupUi

    def retranslateUi(self, SMachineType):
        SMachineType.setWindowTitle(
            QCoreApplication.translate("SMachineType", "Form", None)
        )
        self.in_machine_type.setText(
            QCoreApplication.translate("SMachineType", "Machine type :", None)
        )
        self.c_type.setItemText(
            0, QCoreApplication.translate("SMachineType", "SCIM", None)
        )
        self.c_type.setItemText(
            1, QCoreApplication.translate("SMachineType", "DFIM", None)
        )
        self.c_type.setItemText(
            2, QCoreApplication.translate("SMachineType", "WRSM", None)
        )
        self.c_type.setItemText(
            3, QCoreApplication.translate("SMachineType", "SPMSM", None)
        )
        self.c_type.setItemText(
            4, QCoreApplication.translate("SMachineType", "SIPMSM", None)
        )
        self.c_type.setItemText(
            5, QCoreApplication.translate("SMachineType", "IPMSM", None)
        )
        self.c_type.setItemText(
            6, QCoreApplication.translate("SMachineType", "SyRM", None)
        )

        self.img_type_machine.setText("")
        # if QT_CONFIG(tooltip)
        self.is_inner_rotor.setToolTip(
            QCoreApplication.translate(
                "SMachineType",
                "1 for internal rotor topology, 0 for external rotor",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.is_inner_rotor.setText(
            QCoreApplication.translate("SMachineType", "is_inner_rotor", None)
        )
        self.in_name.setText(
            QCoreApplication.translate("SMachineType", "Machine name :", None)
        )
        self.in_p.setText(QCoreApplication.translate("SMachineType", "p :", None))
        self.b_previous.setText(
            QCoreApplication.translate("SMachineType", "Previous", None)
        )
        self.b_next.setText(QCoreApplication.translate("SMachineType", "Next", None))

    # retranslateUi
