"""User Defined Machine"""

from pyleecan.Classes.MachineUD import MachineUD
from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.Frame import Frame
from pyleecan.Classes.FrameBar import FrameBar
from pyleecan.Classes.Shaft import Shaft
from pyleecan.Classes.Winding import Winding
from pyleecan.Functions.Load.import_class import import_class
from utils.global_functions import convert_list_to_dict, InvalidInputError

def extend_MachineUD():
    """Adds custom ECS methods to Pyleecan MachineIPMSM class"""
    setattr(MachineUD, "json_to_pyleecan", json_to_pyleecan)
    setattr(MachineUD, "check", check)

def check(self, inp):
    """
    Checks if user input from Frontend is valid

    Parameters
    ----------
    self: MachineUD
    inp: dict
        User input from Frontend
    """
    err = []

    rotor = inp["rotor"]
    stator = inp["stator"]
    housing = inp["housing"]

    if rotor["type"] is None:
        err.append("Missing Input: No Rotor defined!")
    elif rotor["type"] == "LamHole":
        if rotor["hole"] is None:
            err.append("Missing Input: No Rotor Hole defined!")
    elif rotor["type"] == "LamSlot":
        if rotor["slot"] is None:
            err.append("Missing Input: No Rotor Slot defined!")
        if rotor["conductor"] is None:
            err.append("Missing Input: No Rotor Conductor defined!")

    if stator["type"] is None:
        err.append("Missing Input: No Stator defined!")
    else:
        if stator["slot"] is None:
            err.append("Missing Input: No Stator Slot defined!")
        if stator["conductor"] is None:
            err.append("Missing Input: No Stator Conductor defined!")

    if housing["type"] is None:
        err.append("Missing Input: No Housing defined!")

    if not err is None:
        err_str = "\n".join(err)
        raise InvalidInputError(err_str)

def json_to_pyleecan(self, inp_dict, material_db=None):
    """
    Creates pyleecan MachineUD object from Frontend json input

    Parameters
    ----------
    self: MachineUD
    inp_dict: json
        Frontend User Input
    material_db: list
        List containing Pyleecan materials. If None, Machine is created without materials.

    Returns
    -------
    machine: MachineUD
        Pyleecan MachineUD object
    """
    #Get required inputs
    inp_rotor = inp_dict["rotor"]
    rotor_type = inp_rotor["type"]
    inp_rotor_lam = inp_rotor["data"]
    inp_hole = inp_rotor.get("hole")
    inp_rotor_slot = inp_rotor.get("slot")
    inp_rotor_cond = inp_rotor.get("conductor")

    inp_stator = inp_dict["stator"]
    inp_stator_lam = inp_stator["data"]
    inp_slot = inp_stator.get("slot")
    inp_cond = inp_stator.get("conductor")

    frame_type = inp_dict["housing"]["type"]
    inp_frame = inp_dict["housing"]["data"]
    if material_db:
        material_dict = convert_list_to_dict(material_db, 'name')
    else:
        material_dict = {}

    #Default values in case machine has only been defined partially
    if inp_hole:
        n_pole = inp_hole["data"]["Zh"]//2
    elif inp_rotor_slot:
        n_pole = inp_rotor_slot["data"]["Zs"]//2
    else:
        n_pole = 2

    #Rotor
    if rotor_type == "LamHole":
        rotor_mat = material_dict.get(inp_rotor_lam["Material"], -1)
        rotor = LamHole(L1=inp_rotor_lam["CoreLength"], Kf1=inp_rotor_lam["PackingFactor"], Rext=inp_rotor_lam["ExternalRadius"], Rint=inp_rotor_lam["InternalRadius"], mat_type=rotor_mat, is_stator=False, is_internal=True)
        if inp_hole:
            mag_mat = material_dict.get(inp_hole["data"]["Material"], -1)
            air_mat = material_dict.get("Air", -1)
            rotor_hole = import_class("pyleecan.Classes", inp_hole["type"])
            rotor_hole = rotor_hole(init_dict=inp_hole["data"], mat_void=air_mat)
            rotor.hole.append(rotor_hole)
            rotor.hole[0].magnet_0.mat_type = mag_mat
    elif rotor_type == "LamSlot":
        rotor_mat = material_dict.get(inp_rotor_lam["Material"], -1)
        rotor = LamSlotWind(L1=inp_rotor_lam["CoreLength"], Kf1=inp_rotor_lam["PackingFactor"], Rext=inp_rotor_lam["ExternalRadius"],
                            Rint=inp_rotor_lam["InternalRadius"], mat_type=rotor_mat, is_stator=False, is_internal=True)
        if inp_rotor_slot:
            rotor_slot = import_class("pyleecan.Classes", inp_rotor_slot.get("type"))
            rotor.slot = rotor_slot(init_dict=inp_rotor_slot["data"])
            rotor.winding = Winding(is_aper_a=True, p=inp_rotor_slot["data"]["Zs"] // 2)  # , init_dict=inp_rotor["Winding"])
        else:
            rotor.slot = None
        if inp_rotor_cond:
            conductor_mat = material_dict.get(inp_rotor_cond["data"]["ConductorMaterial"], -1)
            insulation_mat = material_dict.get(inp_rotor_cond["data"]["InsulationMaterial"], -1)
            rotor_conductor = import_class("pyleecan.Classes", inp_rotor_cond.get("type"))
            rotor.winding.conductor = rotor_conductor(cond_mat=conductor_mat, ins_mat=insulation_mat, init_dict=inp_rotor_cond["data"])
    else:
        rotor = None

    #Stator
    if inp_stator_lam is None:
        stator = None
    else:
        stator_mat = material_dict.get(inp_stator_lam["Material"], -1)
        stator = LamSlotWind(L1=inp_stator_lam["CoreLength"], Kf1=inp_stator_lam["PackingFactor"], Rext=inp_stator_lam["ExternalRadius"], Rint=inp_stator_lam["InternalRadius"], mat_type=stator_mat, is_stator=True, is_internal=False)
        if inp_slot:
            stator_slot = import_class("pyleecan.Classes", inp_slot.get("type"))
            stator.slot = stator_slot(init_dict=inp_slot["data"])
            stator.winding = Winding(is_aper_a=True, p=n_pole)  #, init_dict=inp_stator["Winding"])
        else:
            stator.slot = None
        if inp_cond:
            conductor_mat = material_dict.get(inp_cond["data"]["ConductorMaterial"], -1)
            insulation_mat = material_dict.get(inp_cond["data"]["InsulationMaterial"], -1)
            stator_conductor = import_class("pyleecan.Classes", inp_cond["type"])
            stator.winding.conductor = stator_conductor(cond_mat=conductor_mat, ins_mat=insulation_mat, init_dict=inp_cond["data"])

    #Frame
    if frame_type == "Frame":
        frame_mat = material_dict.get(inp_frame["Material"], -1)
        frame = Frame(Lfra=inp_frame["FrameLength"], Rint=inp_frame["InternalRadius"], Rext=inp_frame["ExternalRadius"], mat_type=frame_mat)
    elif frame_type == "FrameBar":
        frame_mat = material_dict.get(inp_frame["Material"], -1)
        frame = FrameBar(Nbar=inp_frame["NBar"], wbar=inp_frame["WidthBar"], Lfra=inp_frame["FrameLength"], Rint=inp_frame["InternalRadius"],
                         Rext=inp_frame["ExternalRadius"], mat_type=frame_mat)
    else:
        frame = None
    # if inp_frame is None:
    #     frame = None
    # else:
    #     frame_mat = material_dict.get(inp_frame["Material"], -1)
    #     frame = Frame(Lfra=inp_frame["FrameLength"], Rint=inp_frame["InternalRadius"], Rext=inp_frame["ExternalRadius"], mat_type=frame_mat)

    #Shaft
    if inp_rotor_lam is None:
        shaft = None
    else:
        shaft_mat = rotor_mat
        shaft = Shaft(Drsh=inp_rotor_lam["InternalRadius"]*2, Lshaft=None, mat_type=shaft_mat)

    #Create Machine
    machine_dict = {
        "rotor": rotor,
        "stator": stator,
        "frame": frame,
        "shaft": shaft,
        "type_machine": 1
    }
    machine = MachineUD(init_dict=machine_dict, name="Axial View")
    if rotor:
        machine.lam_list.append(rotor)
    if stator:
        machine.lam_list.append(stator)

    return machine
