"""Wound Rotor Synchronous Machine"""

from pyleecan.Classes.MachineWRSM import MachineWRSM
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.FrameBar import FrameBar
from pyleecan.Classes.Shaft import Shaft
from pyleecan.Classes.Winding import Winding
from pyleecan.Functions.Load.import_class import import_class
from utils.global_functions import find_object, convert_list_to_dict

def extend_MachineWRSM():
    """Adds custom ECS methods to Pyleecan MachineWRSM class"""
    setattr(MachineWRSM, "json_to_pyleecan", json_to_pyleecan)

def json_to_pyleecan(self, inp_dict, material_db=None):
    """
    Creates pyleecan MachineWRSM object from Frontend json input

    Parameters
    ----------
    self: MachineWRSM
    inp_dict: json
        Frontend User Input
    material_db: list
        List containing Pyleecan materials. If None, Machine is created without materials.

    Returns
    -------
    machine: MachineWRSM
        Pyleecan MachineWRSM object
    """
    inp_rotor = inp_dict["rotor"]
    inp_rotor_lam = inp_rotor["data"]
    inp_rotor_slot = inp_rotor.get("slot")
    inp_rotor_cond = inp_rotor.get("conductor")
    inp_stator = inp_dict["stator"]
    inp_stator_lam = inp_stator["data"]
    inp_stator_slot = inp_stator.get("slot")
    inp_stator_cond = inp_stator.get("conductor")
    inp_frame = inp_dict["housing"]["data"]
    if material_db:
        material_dict = convert_list_to_dict(material_db, 'name')
    else:
        material_dict = {}

    #Rotor
    rotor_mat = material_dict.get(inp_rotor_lam["Material"], -1)
    rotor = LamSlotWind(L1=inp_rotor_lam["CoreLength"], Kf1=inp_rotor_lam["PackingFactor"], Rext=inp_rotor_lam["ExternalRadius"], Rint=inp_rotor_lam["InternalRadius"], mat_type=rotor_mat, is_stator=False, is_internal=True)
    rotor_slot = import_class("pyleecan.Classes", inp_rotor_slot.get("type"))
    rotor.slot = rotor_slot(init_dict=inp_rotor_slot["data"])
    rotor.winding = Winding(is_aper_a=True, p=inp_rotor_slot["data"]["Zs"]//2) #, init_dict=inp_rotor["Winding"])
    conductor_mat = material_dict.get(inp_rotor_cond["data"]["ConductorMaterial"], -1)
    insulation_mat = material_dict.get(inp_rotor_cond["data"]["InsulationMaterial"], -1)
    rotor_conductor = import_class("pyleecan.Classes", inp_rotor_cond.get("type"))
    rotor.winding.conductor = rotor_conductor(cond_mat=conductor_mat, ins_mat=insulation_mat, init_dict=inp_rotor_cond["data"])

    #Stator
    stator_mat = material_dict.get(inp_stator_lam["Material"], -1)
    stator = LamSlotWind(L1=inp_stator_lam["CoreLength"], Kf1=inp_stator_lam["PackingFactor"], Rext=inp_stator_lam["ExternalRadius"], Rint=inp_stator_lam["InternalRadius"], mat_type=stator_mat, is_stator=True, is_internal=False)
    stator_slot = import_class("pyleecan.Classes", inp_stator_slot.get("type"))
    stator.slot = stator_slot(init_dict=inp_stator_slot["data"])
    stator.winding = Winding(is_aper_a=True, p=inp_rotor_slot["data"]["Zs"]//2) #, init_dict=inp_rotor["Winding"])
    conductor_mat = material_dict.get(inp_stator_cond["data"]["ConductorMaterial"], -1)
    insulation_mat = material_dict.get(inp_stator_cond["data"]["InsulationMaterial"], -1)
    stator_conductor = import_class("pyleecan.Classes", inp_stator_cond.get("type"))
    stator.winding.conductor = stator_conductor(cond_mat=conductor_mat, ins_mat=insulation_mat, init_dict=inp_stator_cond["data"])

    #Frame
    frame_mat = material_dict.get(inp_frame["Material"], -1)
    frame = FrameBar(Nbar=inp_frame["NBar"], wbar=inp_frame["WidthBar"], Lfra=inp_frame["FrameLength"], Rint=inp_frame["InternalRadius"], Rext=inp_frame["ExternalRadius"], mat_type=frame_mat)

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
    self = MachineWRSM(init_dict=machine_dict, name="Axial View")
    return self