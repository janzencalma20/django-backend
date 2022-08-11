# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from ....Functions.init_fig import init_fig


def plot(
    self,
    fig=None,
    ax=None,
    sym=1,
    alpha=0,
    delta=0,
    is_edge_only=False,
    comp_machine=None,
    is_show_fig=True,
    save_path=None,
    win_title=None,
    colors={},
    size=None,
):
    """Plot the Machine in a matplotlib fig

    Parameters
    ----------
    self : Machine
        A Machine object
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        Axis on which to plot the data
    sym : int
        Symmetry factor (1= full machine, 2= half of the machine...)
    alpha : float
        Angle for rotation [rad]
    delta : complex
        Complex value for translation
    is_edge_only: bool
        To plot transparent Patches
    comp_machine : Machine
        A machine to plot in transparency on top of the self machine
    is_show_fig : bool
        To call show at the end of the method
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    colors: dict
        Dictionary containing colour of machine components
    size: tuple
        Size of created figure, defaults to (8,8)
    """
    # (fig, ax, _, _) = init_fig(fig=fig, ax=ax, shape="rectangle")
    (fig, ax, _, _) = init_fig(fig=fig, ax=ax, shape="square", size=size)

    # Call each plot method to properly set the legend
    if self.frame is not None:
        frame_color = colors.get("frame")
        self.frame.plot(
            fig=fig,
            ax=ax,
            sym=sym,
            alpha=alpha,
            delta=delta,
            is_edge_only=is_edge_only,
            is_show_fig=False,
            color=frame_color,
        )
        Wfra = self.frame.comp_height_eq()
    else:
        Wfra = 0

    # Determin order of plotting parts
    lam_list = self.get_lam_list(is_int_to_ext=True)
    if lam_list:
        Rext = lam_list[-1].Rext
    elif self.frame is not None:
        Rext = self.frame.Rint
    else:
        Rext = 0.0

    for lam in lam_list[::-1]:
        lam.plot(
            fig=fig,
            ax=ax,
            sym=sym,
            alpha=alpha,
            delta=delta,
            is_edge_only=is_edge_only,
            is_show_fig=False,
            colors=colors,
        )

    if lam_list and lam_list[0].Rint > 0 and self.shaft is not None:
        shaft_color = colors.get("shaft")
        self.shaft.plot(
            fig=fig,
            ax=ax,
            sym=sym,
            alpha=alpha,
            delta=delta,
            is_edge_only=is_edge_only,
            is_show_fig=False,
            color=shaft_color,
        )

    Lim = (Rext + Wfra) * 1.1  # Axes limit for plot

    if comp_machine is not None:
        comp_machine.rotor.plot(
            fig,
            ax,
            sym=sym,
            alpha=alpha,
            delta=delta,
            is_edge_only=True,
            is_show_fig=is_show_fig,
        )
        comp_machine.stator.plot(
            fig,
            ax,
            sym=sym,
            alpha=alpha,
            delta=delta,
            is_edge_only=True,
            is_show_fig=is_show_fig,
        )

    ax.set_xlabel("(m)")
    ax.set_ylabel("(m)")
    ax.set_title(self.name)

    # Axis Setup
    plt.axis("equal")

    # The Lamination is centered in the figure
    ax.set_xlim(-Lim, Lim)
    ax.set_ylim(-Lim, Lim)

    # Remove Legend
    ax.legend_ = None

    # Add colorbar
    cmap = colors.get("cmap")
    norm = colors.get("norm")
    if colors:
        if cmap and norm:
            color_var = colors.get("var")
            if color_var is None:
                color_var = "Temperature"
            cbar = fig.colorbar(
                mpl.cm.ScalarMappable(cmap=cmap, norm=norm), label=color_var
            )
            cbar.set_ticks(np.linspace(norm.vmin, norm.vmax, 6))
        else:
            print(
                "WARNING: colors were requested to be plotted, but colorbar could not be created as cmap and norm entries are missing in colors dict."
            )

    # Set Windows title
    if self.name not in ["", None] and win_title is None:
        win_title = self.name + " plot machine"

    if save_path is not None:
        fig.savefig(save_path)
        plt.close()

    if is_show_fig:
        fig.show()

    if win_title:
        manager = plt.get_current_fig_manager()
        if manager is not None:
            manager.set_window_title(win_title)
