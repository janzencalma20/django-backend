from os.path import join
import matplotlib.pyplot as plt
from Tests import save_validation_path as save_path
from Tests import TEST_DATA_DIR
from pyleecan.Classes.OPdq import OPdq
from pyleecan.Classes.Simu1 import Simu1

from pyleecan.Classes.DXFImport import DXFImport
from pyleecan.Classes.InputCurrent import InputCurrent

from pyleecan.Classes.MagFEMM import MagFEMM
import pytest
from pyleecan.Functions.load import load
from pyleecan.Functions.Plot import dict_2D
from pyleecan.definitions import DATA_DIR


@pytest.mark.long_5s
@pytest.mark.MagFEMM
@pytest.mark.IPMSM
@pytest.mark.periodicity
@pytest.mark.SingleOP
def test_FEMM_import_dxf():
    """Validation of the TOYOTA Prius electrical machine.

    Test compute the Flux in FEMM, with and without DXF Import
    """
    Toyota_Prius = load(join(DATA_DIR, "Machine", "Toyota_Prius.json"))

    simu = Simu1(name="test_FEMM_import_dxf", machine=Toyota_Prius)

    # Definition of the magnetic simulation (FEMM with symmetry and sliding band)
    simu.mag = MagFEMM(
        type_BH_stator=0,
        type_BH_rotor=0,
        is_periodicity_a=True,
        Kgeo_fineness=0.75,
    )
    # Run only Magnetic module
    simu.force = None
    simu.struct = None

    simu.input = InputCurrent()
    simu.input.OP = OPdq(Id_ref=-100, Iq_ref=200, N0=2000)
    simu.input.Nt_tot = 1  # Number of time step
    simu.input.Na_tot = 2048  # Spatial discretization
    simu.input.rot_dir = 1  # To enforce the rotation direction

    # DXF import setup
    simu.mag.rotor_dxf = DXFImport(
        file_path=join(TEST_DATA_DIR, "prius_test.dxf").replace("\\", "/")
    )
    # Set each surface name
    surf_dict = dict()
    surf_dict[0.0546 + 1j * 0.0224] = "Rotor-0_Lamination"
    surf_dict[0.0763 + 0.00867j] = "Rotor-0_HoleVoid_R0-T0-S0"
    surf_dict[0.0669 + 0.01668j] = "Rotor-0_HoleMag_R0-T0-S0"
    surf_dict[0.0614 + 0.0254j] = "Rotor-0_HoleVoid_R0-T1-S0"
    surf_dict[0.0591 + 0.03555j] = "Rotor-0_HoleMag_R0-T1-S0"
    surf_dict[0.06009 + 0.0478j] = "Rotor-0_HoleVoid_R0-T2-S0"
    simu.mag.rotor_dxf.surf_dict = surf_dict
    # Set every BC
    BC_list = list()
    BC_list.append((0.0489 + 1j * 0.0489, False, "bc_r1"))
    BC_list.append((0, True, "bc_A0"))
    BC_list.append((0.067, False, "bc_r1"))
    simu.mag.rotor_dxf.BC_list = BC_list

    # Run DXF simulation
    out = simu.run()

    # Run Normal simulation
    simu2 = simu.copy()
    simu2.mag.rotor_dxf = None
    out2 = simu2.run()

    # Plot/compare the flux
    out.mag.B.plot_2D_Data(
        "angle{°}",
        data_list=[out2.mag.B],
        legend_list=["Rotor from DXF", "Rotor from pyleecan"],
        save_path=join(save_path, "test_FEMM_import_dxf_B.png"),
        is_show_fig=False,
        **dict_2D
    )


if __name__ == "__main__":
    test_FEMM_import_dxf()
