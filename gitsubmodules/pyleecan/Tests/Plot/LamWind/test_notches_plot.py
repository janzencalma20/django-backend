# -*- coding: utf-8 -*-
from os.path import join

import pytest

import matplotlib.pyplot as plt
from numpy import array, pi, zeros

from pyleecan.Classes.Frame import Frame
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.LamSquirrelCage import LamSquirrelCage
from pyleecan.Classes.MachineDFIM import MachineDFIM
from pyleecan.Classes.Shaft import Shaft
from pyleecan.Classes.VentilationCirc import VentilationCirc
from pyleecan.Classes.VentilationPolar import VentilationPolar
from pyleecan.Classes.VentilationTrap import VentilationTrap
from pyleecan.Classes.Winding import Winding
from pyleecan.Classes.WindingUD import WindingUD
from pyleecan.Classes.SlotW10 import SlotW10
from pyleecan.Classes.SurfLine import SurfLine
from pyleecan.Classes.NotchEvenDist import NotchEvenDist

from Tests import save_plot_path as save_path
from Tests.Plot.LamWind import wind_mat
from pyleecan.Functions.load import load
from pyleecan.definitions import DATA_DIR


def test_LamHole_notch():
    Toyota_Prius = load(join(DATA_DIR, "Machine", "Toyota_Prius.json"))
    slot_r = SlotW10(Zs=8, W0=5e-3, W1=5e-3, W2=5e-3, H0=0, H1=0, H2=2.5e-3)
    notch = NotchEvenDist(notch_shape=slot_r, alpha=pi / 8)
    Toyota_Prius.rotor.notch = [notch]

    Toyota_Prius.plot(is_show_fig=False, save_path=join(save_path, "Toyota_notch.png"))
    Toyota_Prius.plot(
        sym=8, is_show_fig=False, save_path=join(save_path, "Toyota_notch_sym.png")
    )


def test_Lam_evenly_dist():
    """Test machine plot with evenly distributed notches (sym and no sym)"""
    print("\nTest plot Notch")
    plt.close("all")
    test_obj = MachineDFIM()
    test_obj.rotor = LamSlotWind(
        Rint=0.2,
        Rext=0.5,
        is_internal=True,
        is_stator=False,
        L1=0.95,
        Nrvd=1,
        Wrvd=0.05,
    )
    test_obj.rotor.slot = SlotW10(
        Zs=6,
        W0=50e-3,
        W1=90e-3,
        W2=100e-3,
        H0=20e-3,
        H1=35e-3,
        H2=130e-3,
        H1_is_rad=False,
    )
    test_obj.rotor.winding = WindingUD(wind_mat=wind_mat, qs=4, p=4, Lewout=60e-3)
    test_obj.shaft = Shaft(Drsh=test_obj.rotor.Rint * 2, Lshaft=1)

    test_obj.stator = LamSlotWind(
        Rint=0.51,
        Rext=0.8,
        is_internal=False,
        is_stator=True,
        L1=0.95,
        Nrvd=1,
        Wrvd=0.05,
    )
    test_obj.stator.slot = SlotW10(
        Zs=6,
        W0=50e-3,
        W1=80e-3,
        W2=50e-3,
        H0=15e-3,
        H1=25e-3,
        H2=140e-3,
        H1_is_rad=False,
    )
    test_obj.stator.winding = WindingUD(wind_mat=wind_mat, qs=4, p=4, Lewout=60e-3)

    test_obj.frame = None

    # Notches setup
    slot_r = SlotW10(Zs=6, W0=40e-3, W1=40e-3, W2=40e-3, H0=0, H1=0, H2=25e-3)
    notch = NotchEvenDist(notch_shape=slot_r, alpha=0)
    test_obj.rotor.notch = [notch]

    slot_s = SlotW10(Zs=6, W0=80e-3, W1=80e-3, W2=80e-3, H0=0, H1=0, H2=30e-3)
    notch = NotchEvenDist(notch_shape=slot_s, alpha=0.5 * pi / 6)
    test_obj.stator.notch = [notch]

    # Yoke notches
    slot_r = SlotW10(Zs=6, W0=40e-3, W1=40e-3, W2=40e-3, H0=0, H1=0, H2=25e-3)
    notch = NotchEvenDist(notch_shape=slot_r, alpha=0)
    test_obj.rotor.yoke_notch = [notch]

    slot_s = SlotW10(Zs=6, W0=80e-3, W1=80e-3, W2=80e-3, H0=0, H1=0, H2=30e-3)
    notch = NotchEvenDist(notch_shape=slot_s, alpha=0.5 * pi / 6)
    test_obj.stator.yoke_notch = [notch]

    # Plot, save and check
    test_obj.plot(
        sym=1, is_show_fig=False, save_path=join(save_path, "test_Lam_notch_sym_1.png")
    )

    test_obj.stator.plot(
        sym=2, is_show_fig=False, save_path=join(save_path, "test_Lam_notch_sym_2.png")
    )

    test_obj.rotor.notch[0].alpha = 0.5 * pi / 6
    test_obj.rotor.yoke_notch[0].alpha = 0.5 * pi / 6
    test_obj.rotor.plot(
        sym=2, is_show_fig=False, save_path=join(save_path, "test_Lam_notch_sym_3.png")
    )


if __name__ == "__main__":
    test_LamHole_notch()
    test_Lam_evenly_dist()
