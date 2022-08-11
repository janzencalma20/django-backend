"""Generic Plotting Functions"""
import os
import matplotlib as mpl
import boto3

from pyleecan.Classes.MachineUD import MachineUD
from pylee_ext.main import expand_pylee_classes, get_pylee_machine
from utils.global_functions import convert_dict_to_floats, setup_input

def create_axial_slice(machine_dict):
    """
    Checks if machine input is valid and generates 2D axial view of machine

    Parameters
    ----------
    machine_dict: dict
        Machine Input from Frontend

    Returns
    -------
    img_dict: dict
        Contains S3 image location, validity of machine dimensions, error msg (optional)
    """
    expand_pylee_classes()
    convert_dict_to_floats(machine_dict)
    setup_input(machine_dict)
    machine = get_pylee_machine(machine_dict)
    machine = machine.json_to_pyleecan(machine_dict)

    #Convert user input to pyleecan format
    # machine_dict = json.load(os.path.join('Debug', 'machine.json'))
    # material_db = get_material_db(os.path.join(lptn_root, "Input", "Material"))
    # machine = json_to_pyleecan(machine_dict, material_db)

    #Check machine
    valid_machine = True
    try:
        if isinstance(machine, MachineUD):
            machine.check(machine_dict)
        else:
            machine.check()
    except Exception as err:
        valid_machine = False
        err_msg = str(err)

    #Plot machine
    os.makedirs('temp', exist_ok=True)
    img_path = os.path.join('temp', 'MachinePlot.png')
    machine.plot(save_path=img_path, is_show_fig=False)

    #Upload image to S3
    bucket = os.environ["BUCKET_NAME"]
    id = machine_dict['id']
    s3_img_path = f"s3://{bucket}/{id}/MachinePlot.png"
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(img_path, f"{bucket}", f"{id}/MachinePlot.png")

    #Delete Local Plot
    if os.path.exists(img_path):
        os.remove(img_path)

    img_dict = {
        "valid_machine": valid_machine,
        "img_loc": s3_img_path
    }
    if not valid_machine:
        img_dict["error"] = err_msg

    return img_dict

def get_temp_color(t, t_min=0.0, t_max=100.0, cmap='jet'):
    """
    Normalises t for range t_max-t_min and converts it to RGBA color for plotting.

    Parameters
    ----------
    t: float
    t_min: float
    t_max:float
    cmap: str
        matplotlib colormap

    Returns
    -------
    temp_map: rgba tuple
    """
    temp_map = mpl.cm.get_cmap(cmap)
    if t < t_min:
        raise ValueError("Current temperature is below minimum temperature")
    if t > t_max:
        raise ValueError("Current temperature is above maximum temperature")
    t_norm = (t-t_min)/(t_max-t_min)
    return temp_map(t_norm)