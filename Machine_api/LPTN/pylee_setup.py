import os
from pyleecan.Functions.load import load
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.Frame import Frame
from pyleecan.Classes.Shaft import Shaft
from pyleecan.Classes.Winding import Winding
from pyleecan.Functions.Load.import_class import import_class

def convert_dict_to_floats(d):
    """
    Converts all entries in nested dictionary to floats if possible.

    Parameters
    ----------
    d: dict
        Dictionary to be converted
    """
    for key, value in d.items():
        if isinstance(value, dict):
            convert_dict_to_floats(value)
        else:
            try:
                if not isinstance(value, bool):
                    d[key] = float(value)
            except (TypeError, ValueError) as e:
                continue

def make_dir(directory):
    """Creates directory if it doesn't exist yet"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def convert_list_to_dict(lst, key):
    """
    Converts list of object to dict using the supplied object property
    Parameters
    ----------
    lst: List to be converted
    key: Object Property to be used as dict key

    Returns
    -------
    new_dict: Return dictionary
    """
    new_dict = {}
    for elem in lst:
        new_dict[getattr(elem,key)] = elem
    return new_dict

def get_material_db(material_dir):
    """
    Creates pyleecan material database from json files located in material_dir

    Parameters
    ----------
    material_dir: str
        Folder containing material files in json format

    Returns
    -------
    material_db: list
        List containing pyleecan materials
    """

    material_db = []
    for fname in os.listdir(material_dir):
        if fname.endswith('json'):
            path = os.path.join(material_dir, fname)
            material = load(path)
            material_db.append(material)

    return material_db

def json_to_pyleecan(inp_dict, material_db):
    """
    Creates pyleecan MachineIPMSM object from Frontend json input

    Parameters
    ----------
    inp_dict: dict
        Frontend User Input

    Returns
    -------
    machine: MachineIPMSM
        Pyleecan MachineIPMSM object
    """
    #Get required inputs
    inp_rotor = inp_dict["rotor"]
    inp_rotor_lam = inp_rotor["data"]
    inp_hole = inp_rotor.get("hole")
    inp_stator = inp_dict["stator"]
    inp_stator_lam = inp_stator["data"]
    inp_slot = inp_stator.get("slot")
    inp_cond = inp_stator.get("conductor")
    inp_frame = inp_dict["housing"]["data"]
    material_dict = convert_list_to_dict(material_db, 'name')

    #Convert input types
    inp_hole["data"]["Zh"] = int(inp_hole["data"]["Zh"])
    inp_slot["data"]["Zs"] = int(inp_slot["data"]["Zs"])

    #Rotor
    rotor_mat = material_dict[inp_rotor_lam["Material"]]
    rotor = LamHole(L1=inp_rotor_lam["CoreLength"], Kf1=inp_rotor_lam["PackingFactor"], Rext=inp_rotor_lam["ExternalRadius"], Rint=inp_rotor_lam["InternalRadius"], mat_type=rotor_mat, is_stator=False, is_internal=True)
    mag_mat = material_dict[inp_hole["data"]["Material"]]
    air_mat = material_dict["Air"]
    rotor_hole = import_class("pyleecan.Classes", inp_hole["type"])
    rotor_hole = rotor_hole(init_dict=inp_hole["data"], mat_void=air_mat)
    rotor.hole.append(rotor_hole)
    rotor.hole[0].magnet_0.mat_type = mag_mat

    #Stator
    stator_mat = material_dict[inp_stator_lam["Material"]]
    stator = LamSlotWind(L1=inp_stator_lam["CoreLength"], Kf1=inp_stator_lam["PackingFactor"], Rext=inp_stator_lam["ExternalRadius"], Rint=inp_stator_lam["InternalRadius"], mat_type=stator_mat, is_stator=True, is_internal=False)
    stator_slot = import_class("pyleecan.Classes", inp_slot.get("type"))
    stator.slot = stator_slot(init_dict=inp_slot["data"])
    stator.winding = Winding(is_aper_a=True, p=inp_hole["data"]["Zh"]//2)  #, init_dict=inp_stator["Winding"])
    conductor_mat = material_dict[inp_cond["data"]["ConductorMaterial"]]
    insulation_mat = material_dict[inp_cond["data"]["InsulationMaterial"]]
    stator_conductor = import_class("pyleecan.Classes", inp_cond["type"])
    stator.winding.conductor = stator_conductor(cond_mat=conductor_mat, ins_mat=insulation_mat, init_dict=inp_cond["data"])

    #Frame
    frame_mat = material_dict[inp_frame["Material"]]
    frame = Frame(Lfra=inp_frame["FrameLength"], Rint=inp_frame["InternalRadius"], Rext=inp_frame["ExternalRadius"], mat_type=frame_mat)

    #Shaft
    shaft_mat = rotor_mat
    shaft = Shaft(Drsh=inp_rotor_lam["InternalRadius"]*2, Lshaft=None, mat_type=shaft_mat)

    #Create Machine
    machine_dict = {
        "rotor": rotor,
        "stator": stator,
        "frame": frame,
        "shaft": shaft,
        "type_machine": 8
    }
    machine = MachineIPMSM(init_dict=machine_dict, name="Axial View")
    return machine


if __name__ == '__main__':
    pass


