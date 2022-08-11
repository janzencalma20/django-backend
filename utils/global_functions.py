"""Contains generic functions that are used by multiple other modules"""

import os
import jsonpickle
import linecache
import tracemalloc
import boto3

def display_memory_usage(key_type='lineno', limit=10, verbose=False):
    """Displays Total Memory Usage of executed Python code.
    Requires tracemalloc.start() to be executed previously."""
    try:
        snapshot = tracemalloc.take_snapshot()
    except RuntimeError:
        print("Memory Usage could not be computed as memory usage has not been logged (run tracemalloc.start() to monitor memory usage).")
        return None

    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)
    if verbose:
        print("Top %s lines" % limit)
        for index, stat in enumerate(top_stats[:limit], 1):
            frame = stat.traceback[0]
            print("#%s: %s:%s: %.1f KiB"
                  % (index, frame.filename, frame.lineno, stat.size / 1024))
            line = linecache.getline(frame.filename, frame.lineno).strip()
            if line:
                print('    %s' % line)

        other = top_stats[limit:]
        if other:
            size = sum(stat.size for stat in other)
            print("%s other: %.1f MB" % (len(other), size / 1024000))

    total = sum(stat.size for stat in top_stats)
    print("Total Memory Usage: %.1f MB" % (total / 1024000))

def find_object(name, lst, match_attribute='Name', match_type='single', silent=False):
    """
    Returns object in lst whose attribute corresponds to name. Can return one object, or list of objects.

    Parameters
    ----------
    name: str
        Search Value
    lst: list
        List containing Objects to be searched
    match_attribute: str
        Name of attribute to be compared vs name
    match_type: {'single', 'equal', 'partial'}
        single returns one object (exact match required). equal returns list of objects (exact match required). Else returns list of objects (partial match)
    silent: bool
        Prints Warning if True and no matching objects are found in lst

    Returns
    -------
    object, list
        Found object (if single) or list of objects
    """
    if isinstance(lst, dict):
        lst = list(lst.values())
    return_lst = []
    for object in lst:
        object_attr = getattr(object, match_attribute)
        if match_type == 'single':
            if object_attr == name:
                return (object)
        elif match_type == 'equal':
            if isinstance(object_attr, list):
                if any(name==elem for elem in object_attr):
                    return_lst.append(object)
            else:
                if name==object_attr:
                    return_lst.append(object)
        else:
            if isinstance(object_attr, list):
                if any(name in elem for elem in object_attr):
                    return_lst.append(object)
            else:
                if name in object_attr:
                    return_lst.append(object)

    if return_lst == [] and not silent:
        print('WARNING: No matching object found for attribute %s with name %s!' % (match_attribute, name))
    return (return_lst)


def print_object_attributes(obj):
    """Prints all attributes/instances of Class"""
    for attr, value in obj.__dict__.items():
        print('%s: %s' % (attr, value))

def get_headers(fname, sep=None):
    """
    Gets headers from first line in text file

    Parameters
    ----------
    fname: str
        Path of file to be opened
    sep: str
        Column separator, defaults to Tab

    Returns
    -------
    list
        list of column names
    """
    with open(fname) as f:
        labels = f.readline().strip().split(sep)
    return(labels)

def object_to_json(obj, fname, dir_out='JSON'):
    """
    Saves object as JSON file

    Parameters
    ----------
    obj: object
        Object to be saved
    fname: str
        Output Filename
    dir_out: str
        Output directory. Will be created if it does not exist.
    """
    path = dir_out+os.sep+fname
    #Create Output Directory
    if not os.path.isdir(dir_out):
        os.makedirs(dir_out)
    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    with open(path, 'w') as f:
        json_str = jsonpickle.encode(obj)
        # json_str = json.dumps(self.Dictionary, indent=4)
        f.write(json_str)

def convert_list_to_dict(lst, key):
    """
    Converts list of objects to dict using the supplied object property

    Parameters
    ----------
    lst: list
        List to be converted
    key: str
        Object Property to be used as dict key

    Returns
    -------
    new_dict: dict
        Return dictionary
    """
    new_dict = {}
    for elem in lst:
        new_dict[getattr(elem,key)] = elem
    return new_dict

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

def s3_upload_dir(path, bucket='ecscohere', bucket_dir='', filter=None):
    """
    Uploads all files in local directory to s3 bucket

    Parameters
    ----------
    path: str
        Local directory
    bucket: str
        S3 bucket, default: ecscohere
    bucket_dir: str
        Bucket Directory files should be uploaded to. default: top level
    filter: str
        Only uploads files matching filter. default: None
    """
    s3C = boto3.client('s3')
    for root, dirs, files in os.walk(path):
        for file in files:
            if filter:
                if not filter in file:
                    continue

            bucket_path = os.path.join(bucket_dir, file)
            s3C.upload_file(os.path.join(root, file), bucket, bucket_path)

def setup_input(inp):
    """
    Adds additional information to Machine

    Parameters
    ----------
    inp: dict
        Json user input
-
    Returns
    -------
    inp: dict
        Adjusted input dict containing all information necessary to solve lptn
    """
    #Convert wrongly converted floats back to ints
    inp["id"] = int(inp["id"])

    try:
        inp["rotor"]["hole"]["data"]["Zh"] = int(inp["rotor"]["hole"]["data"]["Zh"])
    except Exception:
        pass

    try:
        inp["rotor"]["slot"]["data"]["Zs"] = int(inp["rotor"]["slot"]["data"]["Zs"])
    except Exception:
        pass

    try:
        inp["stator"]["slot"]["data"]["Zs"] = int(inp["stator"]["slot"]["data"]["Zs"])
    except Exception:
        pass

    try:
        inp["housing"]["data"]["NBar"] = int(inp["housing"]["data"]["NBar"])
    except Exception:
        pass

    rotor_type = inp["rotor"]["type"]
    stator_type = inp["stator"]["type"]

    if rotor_type == "LamHole" and stator_type == "LamSlot":
        inp["type"] = "IPMSM"
    elif rotor_type == "LamSlot" and stator_type == "LamSlot":
        inp["type"] = "WRSM"
    else:
        inp["type"] = None
        # raise InvalidInputError(f"ERROR: Unknown combination of Rotor and Stator types. Rotor: {rotor_type} Stator: {stator_type}")

    return inp

def check_input(inp):
    """
    Checks if user has supplied all the required input
    Checks if required input makes sense (To be added)

    Parameters
    ----------
    inp: dict
        Json user input
-
    Returns
    -------
    inp: dict
        Adjusted input dict containing all information necessary to solve lptn
    """
    err = "ERROR:"

    rotor_type = inp["rotor"]["type"]
    stator_type = inp["stator"]["type"]
    housing_type = inp["housing"]["type"]

    if rotor_type is None:
        err += " No Rotor defined."
    if stator_type is None:
        err += " No Stator defined."
    if housing_type is None:
        err += " No Housing defined."

    if rotor_type == "LamHole" and stator_type == "LamSlot":
        inp["type"] = "IPMSM"
    elif rotor_type == "LamSlot" and stator_type == "LamSlot":
        inp["type"] = "WRSM"
    else:
        raise InvalidInputError(f"ERROR: Unknown combination of Rotor and Stator types. Rotor: {rotor_type} Stator: {stator_type}")

class InvalidInputError(Exception):
    """Raise when invalid input is received from Frontend/Database"""


