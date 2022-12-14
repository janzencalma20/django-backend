def comp_FEMM_torque(femm, FEMM_dict, sym=1):
    """Compute the torque of the current FEMM simulation result
    Parameters
    ----------
    femm : FEMMHandler
        client to send command to a FEMM instance
    FEMM_dict : dict
        dict containig FEMM parameters
    """

    # Select rotor groups
    femm.mo_seteditmode("area")
    femm.mo_groupselectblock(FEMM_dict["groups"]["GROUP_RC"])  # rotor core
    femm.mo_groupselectblock(FEMM_dict["groups"]["GROUP_RW"])  # rotor winding
    femm.mo_groupselectblock(FEMM_dict["groups"]["GROUP_RM"])  # rotor magnet
    # sym = 2 => Only half the machine
    return sym * femm.mo_blockintegral(22)
