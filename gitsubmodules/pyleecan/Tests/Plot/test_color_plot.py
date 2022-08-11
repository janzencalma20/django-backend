import os
import matplotlib as mpl
from matplotlib.cm import get_cmap

from pyleecan.Functions.load import load
from pyleecan.definitions import DATA_DIR

def get_temp_color(t, t_min=0.0, t_max=100.0, cmap='jet'):
    temp_map = get_cmap(cmap)
    if t < t_min:
        raise ValueError("Current temperature is below minimum temperature")
    if t > t_max:
        raise ValueError("Current temperature is above maximum temperature")
    t_norm = (t-t_min)/(t_max-t_min)
    return temp_map(t_norm)

def test_color_plot():
    #Get colors
    cmap = mpl.cm.jet
    color_dict = {
        "frame": get_temp_color(30, cmap=cmap),
        "stator": get_temp_color(50, cmap=cmap),
        "rotor": get_temp_color(70, cmap=cmap),
        "shaft": get_temp_color(60, cmap=cmap),
        "winding": get_temp_color(100, cmap=cmap),
        "magnet": get_temp_color(90, cmap=cmap),
        "cmap": cmap,
        "norm": mpl.colors.Normalize(vmin=0, vmax=100),
        "var": "Temperature"
    }

    cwd = os.path.dirname(os.path.abspath(__file__))
    pic_path = os.path.join(cwd, 'ColorTestPlot.png')

    machine = load(os.path.join(DATA_DIR, 'Machine', 'IPMSM_xxx.json'))
    machine.plot(is_show_fig=False, save_path=pic_path, colors=color_dict)

if __name__=='__main__':
    test_color_plot()