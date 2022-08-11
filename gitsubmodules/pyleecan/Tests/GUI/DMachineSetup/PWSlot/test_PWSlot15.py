# -*- coding: utf-8 -*-

import sys
from random import uniform

from PySide2 import QtWidgets
from PySide2.QtTest import QTest

from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.SlotW15 import SlotW15
from pyleecan.GUI.Dialog.DMachineSetup.SWSlot.PWSlot15.PWSlot15 import PWSlot15


import pytest


class TestPWSlot15(object):
    """Test that the widget PWSlot15 behave like it should"""

    @pytest.fixture
    def setup(self):
        """Run at the begining of every test to setup the gui"""

        if not QtWidgets.QApplication.instance():
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = QtWidgets.QApplication.instance()

        test_obj = LamSlotWind(Rint=92.5e-3, Rext=0.2, is_internal=False)
        test_obj.slot = SlotW15(
            H0=0.10, H1=0.11, H2=0.12, W0=0.13, W3=0.14, R1=0.15, R2=0.16
        )
        widget = PWSlot15(test_obj)

        yield {"widget": widget, "test_obj": test_obj}

        self.app.quit()

    def test_init(self, setup):
        """Check that the Widget spinbox initialise to the lamination value"""

        assert setup["widget"].lf_H0.value() == 0.10
        assert setup["widget"].lf_H1.value() == 0.11
        assert setup["widget"].lf_H2.value() == 0.12
        assert setup["widget"].lf_W0.value() == 0.13
        assert setup["widget"].lf_W3.value() == 0.14
        assert setup["widget"].lf_R1.value() == 0.15
        assert setup["widget"].lf_R2.value() == 0.16

    def test_set_H0(self, setup):
        """Check that the Widget allow to update H0"""
        setup["widget"].lf_H0.clear()  # Clear the field before writing
        value = round(uniform(0, 1), 4)
        QTest.keyClicks(setup["widget"].lf_H0, str(value))
        setup["widget"].lf_H0.editingFinished.emit()  # To trigger the slot

        assert setup["widget"].slot.H0 == value

    def test_set_H1(self, setup):
        """Check that the Widget allow to update H1"""
        setup["widget"].lf_H1.clear()  # Clear the field before writing
        value = round(uniform(0, 1), 4)
        QTest.keyClicks(setup["widget"].lf_H1, str(value))
        setup["widget"].lf_H1.editingFinished.emit()  # To trigger the slot

        assert setup["widget"].slot.H1 == value

    def test_set_H2(self, setup):
        """Check that the Widget allow to update H2"""
        setup["widget"].lf_H2.clear()  # Clear the field before writing
        value = round(uniform(0, 1), 4)
        QTest.keyClicks(setup["widget"].lf_H2, str(value))
        setup["widget"].lf_H2.editingFinished.emit()  # To trigger the slot

        assert setup["widget"].slot.H2 == value

    def test_set_W0(self, setup):
        """Check that the Widget allow to update W0"""
        setup["widget"].lf_W0.clear()  # Clear the field before writing
        value = round(uniform(0, 1), 4)
        QTest.keyClicks(setup["widget"].lf_W0, str(value))
        setup["widget"].lf_W0.editingFinished.emit()  # To trigger the slot

        assert setup["widget"].slot.W0 == value

    def test_set_W3(self, setup):
        """Check that the Widget allow to update W3"""
        setup["widget"].lf_W3.clear()  # Clear the field before writing
        value = round(uniform(0, 1), 4)
        QTest.keyClicks(setup["widget"].lf_W3, str(value))
        setup["widget"].lf_W3.editingFinished.emit()  # To trigger the slot

        assert setup["widget"].slot.W3 == value

    def test_set_R1(self, setup):
        """Check that the Widget allow to update R1"""
        setup["widget"].lf_R1.clear()  # Clear the field before writing
        value = round(uniform(0, 1), 4)
        QTest.keyClicks(setup["widget"].lf_R1, str(value))
        setup["widget"].lf_R1.editingFinished.emit()  # To trigger the slot

        assert setup["widget"].slot.R1 == value

    def test_set_R2(self, setup):
        """Check that the Widget allow to update R2"""
        setup["widget"].lf_R2.clear()  # Clear the field before writing
        value = round(uniform(0, 1), 4)
        QTest.keyClicks(setup["widget"].lf_R2, str(value))
        setup["widget"].lf_R2.editingFinished.emit()  # To trigger the slot

        assert setup["widget"].slot.R2 == value

    def test_output_txt(self, setup):
        """Check that the Output text is computed and correct"""
        setup["test_obj"].slot = SlotW15(
            Zs=6, W0=10e-3, W3=30e-3, H0=5e-3, H1=20e-3, H2=50e-3, R1=15e-3, R2=10e-3
        )
        setup["widget"] = PWSlot15(setup["test_obj"])
        assert setup["widget"].w_out.out_slot_height.text() == "Slot height: 0.075 [m]"

    def test_check(self, setup):
        """Check that the check is working correctly"""

        setup["test_obj"] = LamSlotWind(Rint=92.5e-3, Rext=0.2, is_internal=False)
        setup["test_obj"].slot = SlotW15(
            H0=None, H1=0.11, H2=0.12, W0=0.13, W3=0.14, R1=0.15, R2=0.16
        )
        setup["widget"] = PWSlot15(setup["test_obj"])
        assert setup["widget"].check(setup["test_obj"]) == "You must set H0 !"
        setup["test_obj"].slot = SlotW15(
            H0=0.10, H1=None, H2=0.12, W0=0.13, W3=0.14, R1=0.15, R2=0.16
        )
        assert setup["widget"].check(setup["test_obj"]) == "You must set H1 !"
        setup["test_obj"].slot = SlotW15(
            H0=0.10, H1=0.11, H2=None, W0=0.13, W3=0.14, R1=0.15, R2=0.16
        )
        assert setup["widget"].check(setup["test_obj"]) == "You must set H2 !"
        setup["test_obj"].slot = SlotW15(
            H0=0.10, H1=0.11, H2=0.12, W0=None, W3=0.14, R1=0.15, R2=0.16
        )
        assert setup["widget"].check(setup["test_obj"]) == "You must set W0 !"
        setup["test_obj"].slot = SlotW15(
            H0=0.10, H1=0.11, H2=0.12, W0=0.13, W3=None, R1=0.15, R2=0.16
        )
        assert setup["widget"].check(setup["test_obj"]) == "You must set W3 !"
        setup["test_obj"].slot = SlotW15(
            H0=0.10, H1=0.11, H2=0.12, W0=0.13, W3=0.14, R1=None, R2=0.16
        )
        assert setup["widget"].check(setup["test_obj"]) == "You must set R1 !"
        setup["test_obj"].slot = SlotW15(
            H0=0.10, H1=0.11, H2=0.12, W0=0.13, W3=0.14, R1=0.15, R2=None
        )
        assert setup["widget"].check(setup["test_obj"]) == "You must set R2 !"
