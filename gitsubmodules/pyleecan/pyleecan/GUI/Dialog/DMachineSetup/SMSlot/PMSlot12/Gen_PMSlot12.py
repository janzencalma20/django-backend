# -*- coding: utf-8 -*-
"""File generated according to PMSlot12/gen_list.json
WARNING! All changes made in this file will be lost!
"""
from pyleecan.GUI.Dialog.DMachineSetup.SMSlot.PMSlot12.Ui_PMSlot12 import Ui_PMSlot12


class Gen_PMSlot12(Ui_PMSlot12):
    def setupUi(self, PMSlot12):
        """Abstract class to update the widget according to the csv doc"""
        Ui_PMSlot12.setupUi(self, PMSlot12)
        # Setup of in_W0
        txt = self.tr("""Slot isthmus width.""")
        self.in_W0.setWhatsThis(txt)
        self.in_W0.setToolTip(txt)

        # Setup of lf_W0
        self.lf_W0.validator().setBottom(0)
        txt = self.tr("""Slot isthmus width.""")
        self.lf_W0.setWhatsThis(txt)
        self.lf_W0.setToolTip(txt)

        # Setup of in_Wmag
        txt = self.tr("""Magnet width""")
        self.in_Wmag.setWhatsThis(txt)
        self.in_Wmag.setToolTip(txt)

        # Setup of lf_Wmag
        self.lf_Wmag.validator().setBottom(0)
        txt = self.tr("""Magnet width""")
        self.lf_Wmag.setWhatsThis(txt)
        self.lf_Wmag.setToolTip(txt)

        # Setup of in_H0
        txt = self.tr("""Slot isthmus height.""")
        self.in_H0.setWhatsThis(txt)
        self.in_H0.setToolTip(txt)

        # Setup of lf_H0
        self.lf_H0.validator().setBottom(0)
        txt = self.tr("""Slot isthmus height.""")
        self.lf_H0.setWhatsThis(txt)
        self.lf_H0.setToolTip(txt)

        # Setup of in_Hmag
        txt = self.tr("""Magnet Height""")
        self.in_Hmag.setWhatsThis(txt)
        self.in_Hmag.setToolTip(txt)

        # Setup of lf_Hmag
        self.lf_Hmag.validator().setBottom(0)
        txt = self.tr("""Magnet Height""")
        self.lf_Hmag.setWhatsThis(txt)
        self.lf_Hmag.setToolTip(txt)
