# -*- coding: utf-8 -*-

import pytest

from pyleecan.Classes.Segment import Segment
from pyleecan.Classes.SurfLine import SurfLine

from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.HoleM51 import HoleM51

from pyleecan.Classes.Magnet import Magnet
from numpy import exp, arcsin, ndarray, pi

# For AlmostEqual
DELTA = 1e-4

HoleM51_test = list()

test_obj = LamHole(
    Rint=45e-3 / 2, Rext=81.5e-3, is_stator=False, is_internal=True, L1=0.9
)
test_obj.hole = list()
test_obj.hole.append(
    HoleM51(
        Zh=8,
        W0=0.016,
        W1=pi / 6,
        W2=0.004,
        W3=0.01,
        W4=0.002,
        W5=0.01,
        W6=0.002,
        W7=0.01,
        H0=0.01096,
        H1=0.0015,
        H2=0.0055,
    )
)
HoleM51_test.append(
    {
        "test_obj": test_obj,
        "S_exp": 2.917e-4,
        "SM_exp": 1.65e-4,
        "Rmin": 0.06504,
        "Rmax": 0.08,
        "W": 41.411e-3,
        "alpha": 0.487367,
    }
)


class Test_HoleM51_meth(object):
    """pytest for holeB51 methods"""

    @pytest.mark.parametrize("test_dict", HoleM51_test)
    def test_comp_surface(self, test_dict):
        """Check that the computation of the surface is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].comp_surface()

        a = result
        b = test_dict["S_exp"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM51_test)
    def test_comp_surface_mag(self, test_dict):
        """Check that the computation of the magnet surface is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].comp_surface_magnets()

        a = result
        b = test_dict["SM_exp"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM51_test)
    def test_comp_alpha(self, test_dict):
        """Check that the computation of the alpha is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].comp_alpha()

        a = result
        b = test_dict["alpha"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM51_test)
    def test_comp_width(self, test_dict):
        """Check that the computation of width is correct"""
        test_obj = test_dict["test_obj"]

        a = test_obj.hole[0].comp_width()
        b = test_dict["W"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM51_test)
    def test_comp_radius(self, test_dict):
        """Check that the computation of the radius is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].comp_radius()

        a = result[0]
        b = test_dict["Rmin"]
        msg = "For Rmin: Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

        a = result[1]
        b = test_dict["Rmax"]
        msg = "For Rmax: Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM51_test)
    def test_build_geometry_with_magnet(self, test_dict):
        """Check that the surf list is correct with magnet"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].build_geometry()

        assert len(result) == 7
        for surf in result:
            assert type(surf) == SurfLine

        assert result[0].label == "Rotor_HoleVoid_R0-T0-S0"
        assert len(result[0].line_list) == 4

        assert result[1].label == "Rotor_HoleMag_R0-T0-S0"
        assert len(result[1].line_list) == 4

        assert result[2].label == "Rotor_HoleVoid_R0-T1-S0"
        assert len(result[2].line_list) == 6

        assert result[3].label == "Rotor_HoleMag_R0-T1-S0"
        assert len(result[3].line_list) == 4

        assert result[4].label == "Rotor_HoleVoid_R0-T2-S0"
        assert len(result[4].line_list) == 6

        assert result[5].label == "Rotor_HoleMag_R0-T2-S0"
        assert len(result[5].line_list) == 4

        assert result[6].label == "Rotor_HoleVoid_R0-T3-S0"
        assert len(result[6].line_list) == 4

    @pytest.mark.parametrize("test_dict", HoleM51_test)
    def test_build_geometry_no_magnet(self, test_dict):
        """Check that the surf list is correct without magnet"""
        test_obj = LamHole(init_dict=test_dict["test_obj"].as_dict())
        test_obj.hole[0].magnet_0 = None
        test_obj.hole[0].magnet_1 = None
        test_obj.hole[0].magnet_2 = None
        result = test_obj.hole[0].build_geometry()

        assert len(result) == 1
        for surf in result:
            assert type(surf) == SurfLine

        assert result[0].label == "Rotor_HoleVoid_R0-T0-S0"
        assert len(result[0].line_list) == 8

    @pytest.mark.parametrize("test_dict", HoleM51_test)
    def test_build_geometry_simplified_parallel(self, test_dict):
        """Check that the build geometry method works"""

        # is_simplified to True and magnetization Parallel

        test_obj = test_dict["test_obj"]
        test_obj.hole[0].magnet_0 = Magnet(type_magnetization=1)
        test_obj.hole[0].magnet_1 = Magnet(type_magnetization=1)
        test_obj.hole[0].magnet_2 = Magnet(type_magnetization=1)
        a = test_obj.hole[0].build_geometry(is_simplified=True)

        assert a[1].label == "Rotor_HoleMag_R0-T0-S0"
        assert a[1].line_list[0] is not None
        assert a[1].line_list[1] is not None
        with pytest.raises(IndexError) as context:
            a[1].line_list[2]

        assert a[3].label == "Rotor_HoleMag_R0-T1-S0"
        assert a[3].line_list[0] is not None
        assert a[3].line_list[1] is not None
        with pytest.raises(IndexError) as context:
            a[3].line_list[2]

        assert a[5].label == "Rotor_HoleMag_R0-T2-S0"
        assert a[5].line_list[0] is not None
        assert a[5].line_list[1] is not None
        with pytest.raises(IndexError) as context:
            a[5].line_list[2]

    @pytest.mark.parametrize("test_dict", HoleM51_test)
    def test_build_geometry_Z6(self, test_dict):
        """Check if Z6 is different between Zint[0].real > 0 or Zint[1].real > 0"""

        test_obj = test_dict["test_obj"]

        # Zint[1].real > 0
        test_obj.hole[0] = HoleM51(
            Zh=8,
            W0=0.016,
            W1=pi / 6,
            W2=0.004,
            W3=0.01,
            W4=0.002,
            W5=0.01,
            W6=0.002,
            W7=0.01,
            H0=0.01096,
            H1=0.0015,
            H2=0.1055,
        )
        lst = test_obj.hole[0].build_geometry()

        # Zint[0].real > 0
        test_obj.hole[0] = HoleM51(
            Zh=8,
            W0=0.016,
            W1=pi / 65,
            W2=0.004,
            W3=0.01,
            W4=0.002,
            W5=0.01,
            W6=0.002,
            W7=0.01,
            H0=0.01096,
            H1=0.0015,
            H2=0.0055,
        )
        lst2 = test_obj.hole[0].build_geometry()

        assert len(lst) == 7
        assert lst[0].line_list[1].begin != lst2[0].line_list[1].begin

    def test_comp_surface_magnet_id(self):
        """Check that the computation of the magnet surface is correct"""
        test_obj = LamHole(
            Rint=45e-3 / 2, Rext=81.5e-3, is_stator=False, is_internal=True, L1=0.9
        )
        test_obj.hole = list()
        test_obj.hole.append(
            HoleM51(
                Zh=8,
                W0=0.016,
                W1=pi / 6,
                W2=0.004,
                W3=0.01,
                W4=0.002,
                W5=0.01,
                W6=0.002,
                W7=0.01,
                H0=0.01096,
                H1=0.0015,
                H2=0.0055,
            )
        )
        result = test_obj.hole[0].comp_surface_magnet_id(5)
        assert result == 0
