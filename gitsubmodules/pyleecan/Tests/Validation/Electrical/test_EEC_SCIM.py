from os.path import join
from multiprocessing import cpu_count

from pyleecan.Functions.load import load
from pyleecan.definitions import DATA_DIR

from pyleecan.Classes.Simu1 import Simu1
from pyleecan.Classes.OPslip import OPslip
from pyleecan.Classes.Electrical import Electrical
from pyleecan.Classes.EEC_SCIM import EEC_SCIM
from pyleecan.Classes.InputCurrent import InputCurrent

from numpy import angle, cos
import pytest


@pytest.mark.long_5s
@pytest.mark.EEC_SCIM
@pytest.mark.SCIM
@pytest.mark.periodicity
@pytest.mark.SingleOP
@pytest.mark.skip(reason="Work in progress")
def test_EEC_SCIM():
    """Validation of the SCIM Electrical Equivalent Circuit with the 3kW SCIM
    from 'Berechnung elektrischer Maschinen' (ISBN: 978-3-527-40525-1)
    Note: conductor properties have been set to operation point temperature condition,
    stator end winding length is adapted to ref. lenght
    """
    SCIM = load(join(DATA_DIR, "Machine", "SCIM_010.json"))

    # Definition of the electrical simulation
    simu = Simu1(name="test_EEC_SCIM", machine=SCIM)

    # electrical parameter estimation (N0, felec, ... are independent of elec. simu.)
    eec_scim = EEC_SCIM()
    eec_scim.is_periodicity_a = True
    eec_scim.I = 2
    eec_scim.N0 = 1500
    eec_scim.felec = 50
    eec_scim.Nrev = 1 / 6
    eec_scim.Nt_tot = 8
    eec_scim.nb_worker = cpu_count()

    simu.elec = Electrical(
        eec=eec_scim,
    )

    # direct input
    # eec_scim.parameters = {
    #     "Lm": 0.6106,
    #     # 'Lm_': 0.6077,
    #     "Lr_norm": 0.0211,
    #     "Ls": 0.0154,
    #     "Rfe": None,
    #     "slip": None,
    # }

    # Run only Electrical module
    simu.mag = None
    simu.force = None
    simu.struct = None

    # Definition of a sinusoidal current
    simu.input = InputCurrent()
    simu.input.OP = OPslip(
        felec=50, Id_ref=None, Iq_ref=None, Ud_ref=400, Uq_ref=0, N0=1418
    )
    simu.input.Nt_tot = 360  # Number of time steps
    simu.input.Na_tot = 2048  # Spatial discretization
    simu.input.rot_dir = 1  # To enforce the rotation direction
    simu.input.Nrev = 5

    simu.run()

    # Reference
    Lm = 0.6175  # Xm = 194 Ohm @ 50 Hz
    Ls = 0.02203  # Xs = 6.92 Ohm
    Lr_norm = 0.02365  # Xr_norm = 7.43 Ohm
    Rs = 7.23
    Rr_norm = 6.70

    # check with arbitary 2% rel. diff.
    assert abs(eec_scim.parameters["Lm"] - Lm) / Lm <= 0.02
    assert abs(eec_scim.parameters["Lm_"] - Lm) / Lm <= 0.02
    assert abs(eec_scim.parameters["Rr_norm"] - Rr_norm) / Rr_norm <= 0.02
    assert abs(eec_scim.parameters["Rs"] - Rs) / Rs <= 0.02

    # TODO add stray parameter as soon as RMS is avialable
    # TODO compare (joule) losses

    """
    # compute some quantites
    Us = out.elec.Ud_ref + 1j * out.elec.Uq_ref
    Is = out.elec.Id_ref + 1j * out.elec.Iq_ref

    PF = cos(angle(Us) - angle(Is))

    # --- Print voltage and torque ---
    print("Ud: " + str(abs(Us)))
    print("Uq: " + str(abs(Is)))
    print("PF: " + str(PF))

    print("Tem: " + str(out.elec.Tem_av_ref))

    # Plot the currents and plot the voltages
    out.elec.get_Is().plot_2D_Data("time", "phase")
    out.elec.Ir.plot_2D_Data("time", "phase[0]")
    out.elec.Us.plot_2D_Data("time", "phase")
    """


if __name__ == "__main__":
    test_EEC_SCIM()
