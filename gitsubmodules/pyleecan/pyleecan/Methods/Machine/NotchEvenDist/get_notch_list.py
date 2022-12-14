from numpy import pi


def get_notch_list(self, sym=1, is_yoke=False):
    """Returns an ordered description of the notches

    Parameters
    ----------
    self : NotchEvenDist
        A NotchEvenDist object
    sym: int
        Number of symmetry
    is_yoke : bool
        True if the notch is on the Yoke

    Returns
    -------
    notch_list : list
        list of dictionary with key: "begin_angle", "end_angle", "obj"
    """

    notch_list = list()
    if is_yoke:
        self.parent.is_internal = not self.parent.is_internal
        op = self.notch_shape.comp_angle_opening()
        self.parent.is_internal = not self.parent.is_internal
    else:
        op = self.notch_shape.comp_angle_opening()

    for ii in range(self.notch_shape.Zs // sym):
        notch_dict = dict()
        notch_dict["begin_angle"] = (
            2 * pi / self.notch_shape.Zs * ii + self.alpha - op / 2
        )
        notch_dict["end_angle"] = (
            2 * pi / self.notch_shape.Zs * ii + self.alpha + op / 2
        )
        notch_dict["obj"] = self.notch_shape
        notch_list.append(notch_dict)

    return notch_list
