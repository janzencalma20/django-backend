# -*- coding: utf-8 -*-
from .Save.save_json import save_json
from .Save.save_hdf5 import save_hdf5
from .Save.save_pkl import save_pkl


class FormatError(Exception):
    pass


def save(self, save_path="", is_folder=False, type_handle_old=2, type_compression=0):
    """Save the object to the save_path

    Parameters
    ----------
    self :
        A pyleecan object
    save_path: str
        path to the folder to save the object
    is_folder: bool
        to split the object in different files: separate simulation machine and materials (json only)
    type_handle_old : int
        How to handle old file in folder mode (0:Nothing, 1:Delete, 2:Move to "Backup" folder)
    type_compression: int
        Available only for json, 0: no compression, 1: gzip
    """
    # Save in the object.path if it exist and save_path is empty
    if save_path == "" and hasattr(self, "path") and getattr(self, "path") != None:
        save_path = self.path
    if (
        not save_path.endswith("json")
        and not save_path.endswith("h5")
        and not save_path.endswith("pkl")
        and not is_folder
    ):
        save_path += ".json"  # Default format

    # Avoid errors like "\t" in path
    save_path = save_path.replace("\\", "/")
    # Save in json
    if save_path.endswith(".json") or is_folder:
        save_json(
            self,
            save_path=save_path,
            is_folder=is_folder,
            type_handle_old=type_handle_old,
            type_compression=type_compression,
        )
    # Save in hdf5
    elif save_path.endswith(".h5"):
        save_hdf5(self, save_path=save_path)
    # Save in pkl
    elif save_path.endswith(".pkl"):
        save_pkl(self, save_path=save_path)
    else:
        raise FormatError(
            "Unknown file extension: '{}'".format(save_path.rsplit(".")[-1])
        )
