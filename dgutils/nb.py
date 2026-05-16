# A simple helper which collects notebook useful methods

import ipywidgets as widgets
from IPython.display import display
import __main__

_banner = None


def init_banner():
    global _banner

    if _banner is None:
        _banner = widgets.HTML(value="")
        display(_banner)

    return _banner


def set_variable(name, value, units="Å"):
    global _banner

    if _banner is None:
        _banner = init_banner()

    setattr(__main__, name, value)

    _banner.value = f"""
    <div style='background-color:green;
                color:white;
                font-size:20px;
                padding:10px;
                text-align:center;
                font-weight:bold;'>
        ⚠️ {name} = {value} {units} ⚠️
    </div>
    """
