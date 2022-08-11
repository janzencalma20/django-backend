# -*- coding: utf-8 -*-

from matplotlib.pyplot import subplots
import mpl_toolkits.mplot3d
from numpy import array


def init_fig(fig=None, ax=None, shape="default", is_3d=False, size=None):
    """Get all the handle and legend of a figure or initialize them
    (for matplotlib)

    Parameters
    ----------
    fig : Matplotlib.figure.Figure
        The figure to get the handle from (can be None)
    ax : Matplotlib.axes.Axes object
        Axis on which to plot the data
    shape : str
        Shape of the figure: "default", "square" or "rectangle" for 20x10 figure
    is_3d : bool
        3D or 2D figure
    size: tuple
        Size of created figure, defaults to (8,4) for shape=rectangle and (8,8) for shape=square

    Returns
    -------
    (fig,axes,patch_leg,label_leg): Matplotlib.figure.Figure, matplotlib.axes._subplots.AxesSubplot, patch, string
        Figure handle, Axes Handle, List of legend patches, List of legend label

    """
    if fig is None:
        # Create a new figure with empty legend
        if shape == "rectangle":
            if not size:
                size = (8, 4)
            if is_3d:
                fig, axes = subplots(
                    tight_layout=True,
                    figsize=size,
                    subplot_kw=dict(projection="3d"),
                )
            else:
                fig, axes = subplots(tight_layout=True, figsize=size)
        elif shape == "square":
            if not size:
                size = (8, 8)
            if is_3d:
                fig, axes = subplots(
                    tight_layout=True,
                    figsize=size,
                    subplot_kw=dict(projection="3d"),
                )
            else:
                fig, axes = subplots(tight_layout=True, figsize=size)
        else:
            if is_3d:
                fig, axes = subplots(
                    tight_layout=True, subplot_kw=dict(projection="3d")
                )
            else:
                fig, axes = subplots(tight_layout=True)
        patch_leg, label_leg = [], []
    else:
        if ax is None:
            axes = fig.axes[0]
        else:
            axes = ax
        if axes.legend_ is None:
            # Empty legend
            patch_leg, label_leg = [], []
        else:
            # Get the symbol and label of all legend entry
            patch_leg = axes.legend_.get_patches()
            label_leg = [t.get_text() for t in axes.legend_.get_texts()]

    return (fig, axes, patch_leg, label_leg)


def init_subplot(fig=None, subplot_index=None, is_3d=False):
    """Initialize subplot (given position or automatic stacking)

    Parameters
    ----------
    fig : Matplotlib.figure.Figure
        The figure to get the handle from (can be None)
    subplot_index : int
        Index of the subplot, or None
    is_3d : bool
        3D or 2D figure

    Returns
    -------
    (fig,ax): Matplotlib.figure.Figure, matplotlib.axes._subplots.AxesSubplot
        Figure handle, Axes Handle

    """
    is_newfig = False
    if fig is None:
        is_newfig = True

    is_autostack = False
    if subplot_index is None:
        is_autostack = True

    (fig, axes, patch_leg, label_leg) = init_fig(fig, shape="rectangle", is_3d=is_3d)

    if not is_newfig and is_autostack:
        n = len(fig.axes)
        for i in range(n):
            fig.axes[i].change_geometry(n, 1, i)
        if is_3d:
            ax = fig.add_subplot(n, 1, n, projection="3d")
        else:
            ax = fig.add_subplot(n, 1, n)
    else:
        if subplot_index is None:
            subplot_index = 0
        ax = fig.axes[subplot_index]

    return fig, ax
