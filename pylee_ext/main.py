from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineWRSM import MachineWRSM
from pyleecan.Classes.MachineUD import MachineUD

from utils.global_functions import InvalidInputError
from .MachineIPMSM import extend_MachineIPMSM
from .MachineWRSM import extend_MachineWRSM
from .MachineUD import extend_MachineUD

def expand_pylee_classes():
    """Adds additional methods to default pyleecan Classes"""
    #Machines
    extend_MachineIPMSM()
    extend_MachineWRSM()
    extend_MachineUD()

def get_pylee_machine(inp):
    """
    Returns pyleecan machine object corresponding to type
    Returns MachineUD if machine is only partially defined

    Parameters
    ----------
    inp: dict
        Json user input

    Returns
    -------
    machine: Machine
    """
    if inp["housing"]["type"] is None or inp["rotor"]["type"] is None or inp["stator"]["type"] is None:
        return MachineUD()

    machine_type = inp["type"]
    if machine_type =="IPMSM":
        return MachineIPMSM()
    elif machine_type =="WRSM":
        return MachineWRSM()
    else:
        raise InvalidInputError(f"ERROR: Machine Type ({machine_type}) could not be identified")
