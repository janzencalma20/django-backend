# -*- coding: utf-8 -*-


def comp_height_gap(self):
    """Computation of the Height of the gap between the Frame and Outer Lamination

    Parameters
    ----------
    self : FrameBar
        A FrameBar object

    Returns
    -------
    Hgap: float
        Height of the Gap [m], Default: Height of the Frame

    """
    if self.parent.get_lam_list():
        lam_outer = self.parent.get_lam_list()[-1]
        return self.Rint - lam_outer.Rext
    else:
        return self.Rext - self.Rint
