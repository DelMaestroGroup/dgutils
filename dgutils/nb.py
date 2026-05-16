# A simple helper which collects notebook useful methods

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import __main__

_banner_out = widgets.Output()
_displayed = False


def init_banner():
    global _displayed

    if not _displayed:
        display(_banner_out)
        _displayed = True

    return _banner_out


def set_variable(name, value, units="Å"):
    init_banner()

    setattr(__main__, name, value)

    html = f"""
    <div style='background-color:green;
                color:white;
                font-size:20px;
                padding:10px;
                text-align:center;
                font-weight:bold;'>
        ⚠️ {name} = {value} {units} ⚠️
    </div>
    """

    with _banner_out:
        clear_output(wait=True)
        display(HTML(html))
