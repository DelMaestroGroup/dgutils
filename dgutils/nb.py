# A simple helper which collects notebook useful methods

import __main__

_DISPLAY_ID = "notebook_variable_banner"


def set_variable(name, value, units="Å"):
    from IPython.display import display, HTML

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

    display(HTML(html), display_id=_DISPLAY_ID)
