import os
import json
from .pylee_setup import get_material_db, json_to_pyleecan, convert_dict_to_floats
# from pylee_setup import get_material_db, json_to_pyleecan, convert_dict_to_floats
import boto3

lptn_root = os.path.dirname(os.path.realpath(__file__))

def create_machine_image(machine_dict):
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
    convert_dict_to_floats(machine_dict)

    #Convert user input to pyleecan format
    # machine_dict = json.load(os.path.join('Debug', 'machine.json'))
    material_db = get_material_db(os.path.join(lptn_root, "Input", "Material"))
    machine = json_to_pyleecan(machine_dict, material_db)

    #Check machine
    valid_machine = True
    try:
        machine.check()
    except Exception as err:
        valid_machine = False
        err_msg = repr(err)

    #Plot machine
    dir_results = os.path.join(lptn_root, 'Results', 'OtherPlots')
    os.makedirs(dir_results, exist_ok=True)
    img_path = os.path.join(dir_results, 'MachinePlot.png')
    machine.plot(save_path=img_path, is_show_fig=False)

    #Upload image to S3
    bucket = os.environ["BUCKET_NAME"]
    id = int(machine_dict['id'])
    s3_img_path = f"s3://{bucket}/Images/MachinePlot_{id}.png"
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(img_path, f"{bucket}", f"Images/MachinePlot_{id}.png")

    img_dict = {
        "valid_machine": valid_machine,
        "img_loc": s3_img_path
    }
    if not valid_machine:
        img_dict["error"] = err_msg

    return img_dict

###############Main###############
if __name__ == '__main__':
    inp_json = os.path.join("..", "..", "Debug", "machine.json")
    with open(inp_json, 'r') as f:
        inp_dict = json.load(f)
    response = create_machine_image(inp_dict)
    print(f"Image Location: {response}")







