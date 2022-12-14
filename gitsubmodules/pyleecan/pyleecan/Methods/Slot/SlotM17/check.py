# -*- coding: utf-8 -*-

from numpy import pi

from ....Methods.Slot.Slot import SlotCheckError


def check(self):
    """Check that the SlotM17 object is correct

    Parameters
    ----------
    self : SlotM17
        A SlotM17 object

    Returns
    -------
    None
    """
    if self.parent is None:
        raise SlotCheckError("SlotM17 must be inside a lamination")
    if self.Zs != 2:
        raise SlotCheckError("SlotM17 must have p=1")
    if not self.parent.is_internal:
        raise SlotCheckError("SlotM17 must be inside an internal lamination")
