def get_data_from_str(self, data_str):
    """Return the data object corresponding to the data str

    Parameters
    ----------
    self : Output
        an Output object
    data_str : string
        a string corresponding to a data object

    Returns
    -------
    data : Data
        a Data object

    """

    # Get Data object names
    phys = getattr(self, data_str.split(".")[0])
    if "get_" in data_str.split(".")[1]:  # get method
        if "[" in data_str.split(".")[1]:  # dict
            d = getattr(phys, data_str.split(".")[1].split("[")[0])()
            data = d[data_str.split("[")[1].rstrip("]")]
        else:
            data = getattr(phys, data_str.split(".")[1])()
    elif "[" in data_str.split(".")[1]:  # dict
        d = getattr(phys, data_str.split(".")[1].split("[")[0])
        data = d[data_str.split(".")[1].split("[")[1].rstrip("]")]
    else:
        data = getattr(phys, data_str.split(".")[1])

    # If dict with no specified key -> take first key
    if isinstance(data, dict):
        data2 = data[list(data.keys())[0]]
    else:
        data2 = data

    return data2
