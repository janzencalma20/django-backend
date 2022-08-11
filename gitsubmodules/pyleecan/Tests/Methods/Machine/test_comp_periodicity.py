import pytest
from os.path import join

from pyleecan.Functions.load import load
from pyleecan.definitions import DATA_DIR
from pyleecan.Classes.VentilationCirc import VentilationCirc

test_per_list = [
    {"machine": "Toyota_Prius", "exp": (4, True, 4, True)},
    {"machine": "BMW_i3", "exp": (6, True, 6, True)},
    {"machine": "Protean_InWheel", "exp": (8, False, 32, True)},
    {"machine": "Tesla_S", "exp": (2, False, 2, False)},
    {"machine": "Audi_eTron", "exp": (2, False, 2, False)},
    {"machine": "Benchmark", "exp": (1, True, 5, True)},
    {"machine": "SCIM_001", "exp": (1, True, 1, True)},
    {"machine": "SCIM_006", "exp": (2, True, 2, True)},
    {"machine": "SPMSM_001", "exp": (4, False, 4, True)},
    {"machine": "SPMSM_003", "exp": (1, True, 1, True)},
    {"machine": "SPMSM_015", "exp": (9, False, 9, True)},
    {"machine": "SIPMSM_001", "exp": (1, False, 2, True)},
    {"machine": "SynRM_001", "exp": (2, True, 2, True)},
    {"machine": "LSRPM_001", "exp": (4, False, 4, True)},
]

# Machine with ventilation
TP = load(join(DATA_DIR, "Machine", "Toyota_Prius.json"))
# Only Zh matters for periodicity comp
H0 = 0.1235
D0 = 0.01
v2 = VentilationCirc(Zh=2, D0=D0, H0=H0)
v4 = VentilationCirc(Zh=4, D0=D0, H0=H0)
v8 = VentilationCirc(Zh=8, D0=D0, H0=H0)
v9 = VentilationCirc(Zh=9, D0=D0, H0=H0)
v16 = VentilationCirc(Zh=16, D0=D0, H0=H0)

# Rotor vent matches sym
TP0 = TP.copy()
TP0.name = TP0.name + "_0"
TP0.rotor.axial_vent = [v8]
test_per_list.append({"machine": TP0, "exp": (4, True, 4, True)})

# Two Rotor vents that match sym
TP1 = TP.copy()
TP1.name = TP1.name + "_1"
TP1.rotor.axial_vent = [v16, v8]
test_per_list.append({"machine": TP1, "exp": (4, True, 4, True)})

# Rotor vents that with 1/2 sym
TP2 = TP.copy()
TP2.name = TP2.name + "_2"
TP2.rotor.axial_vent = [v8, v4]
test_per_list.append({"machine": TP2, "exp": (4, False, 4, False)})

# Rotor vent that removes sym
TP3 = TP.copy()
TP3.name = TP3.name + "_3"
TP3.rotor.axial_vent = [v9]
test_per_list.append({"machine": TP3, "exp": (1, False, 1, False)})

# Stator vent matches sym
TP4 = TP.copy()
TP4.name = TP4.name + "_4"
TP4.stator.axial_vent = [v8]
test_per_list.append({"machine": TP4, "exp": (4, True, 4, True)})

# Two Stator vents that match sym
TP5 = TP.copy()
TP5.name = TP5.name + "_5"
TP5.stator.axial_vent = [v16, v8]
test_per_list.append({"machine": TP5, "exp": (4, True, 4, True)})

# Stator vents that with 1/2 sym
TP6 = TP.copy()
TP6.name = TP6.name + "_6"
TP6.stator.axial_vent = [v8, v4]
test_per_list.append({"machine": TP6, "exp": (4, False, 4, True)})

# Stator vent that removes sym
TP7 = TP.copy()
TP7.name = TP7.name + "_7"
TP7.stator.axial_vent = [v9]
test_per_list.append({"machine": TP7, "exp": (1, False, 4, True)})

# No sym, remove antiper
SC = load(join(DATA_DIR, "Machine", "SCIM_001.json"))
v9 = v9.copy()
v9.H0 = 0.06
v9.D0 = 0.01
SC0 = SC.copy()
SC0.name = SC0.name + "_0"
SC0.rotor.axial_vent = [v9]
test_per_list.append({"machine": SC0, "exp": (1, False, 1, False)})

# Rotor is 4, True => 1, True
SP = load(join(DATA_DIR, "Machine", "SPMSM_001.json"))
v2 = v2.copy()
v2.H0 = 0.018
v2.D0 = 0.005
SP0 = SP.copy()
SP0.name = SP0.name + "_0"
SP0.rotor.axial_vent = [v2]
test_per_list.append({"machine": SP0, "exp": (2, False, 2, False)})

# no antiper, remove sym
SP1 = SP.copy()
v9 = v9.copy()
v9.H0 = 0.018
v9.D0 = 0.005
SP1.name = SP1.name + "_1"
SP1.rotor.axial_vent = [v9]
test_per_list.append({"machine": SP1, "exp": (1, False, 1, False)})


@pytest.mark.periodicity
@pytest.mark.parametrize("test_dict", test_per_list)
def test_comp_periodicity(test_dict):

    if isinstance(test_dict["machine"], str):
        machine_obj = load(join(DATA_DIR, "Machine", test_dict["machine"] + ".json"))
    else:
        machine_obj = test_dict["machine"]

    per_a, aper_a = machine_obj.comp_periodicity_spatial()

    per_t, aper_t, _, _ = machine_obj.comp_periodicity_time()

    # Check angular
    msg_a = (
        "Wrong Angular periodicity calculation for "
        + machine_obj.name
        + ": Returned "
        + str((per_a, aper_a))
        + " Expected "
        + str((test_dict["exp"][0], test_dict["exp"][1]))
    )
    assert (per_a, aper_a) == (test_dict["exp"][0], test_dict["exp"][1]), msg_a
    # Check time
    msg_t = (
        "Wrong Time periodicity calculation for "
        + machine_obj.name
        + ": Returned "
        + str((per_t, aper_t))
        + " Expected "
        + str((test_dict["exp"][2], test_dict["exp"][3]))
    )
    assert (per_t, aper_t) == (test_dict["exp"][2], test_dict["exp"][3]), msg_t

    return (per_a, aper_a, per_t, aper_t)


# To run it without pytest
if __name__ == "__main__":
    # TP7.plot()
    # SC0.plot()
    # SP0.plot()
    for ii, test_dict in enumerate(test_per_list):
        if isinstance(test_dict["machine"], str):
            machine_name = test_dict["machine"]
        else:
            machine_name = test_dict["machine"].name
        print(str(ii) + " :" + machine_name)
        per_tuple = test_comp_periodicity(test_dict)
    print("Done")

    # per_tuple = test_comp_periodicity(test_per_list[22])
