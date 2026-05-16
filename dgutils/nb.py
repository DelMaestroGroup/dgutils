# A simple helper which collects notebook useful methods

import ipywidgets as widgets
from IPython.display import display

# Module-level state
_banner = None

def _ensure_banner():
    global _banner

    if _banner is None:
        _banner = widgets.HTML(value="")
        display(_banner)


def set_variable(name, value, units="Å"):
    """
    Set a global variable in the notebook namespace and display a banner.
    """

    _ensure_banner()

    # Inject into notebook globals
    import __main__
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
