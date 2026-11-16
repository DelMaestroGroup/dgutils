# dgutils
A python package implenting useful utilities used by the Del Maestro Group

## Installation
    pip install git+https://github.com/DelMaestroGroup/dgutils.git#egg=dgutils

For notebook banners and HTML export, install the optional notebook dependencies:

    python -m pip install 'dgutils[notebook] @ git+https://github.com/DelMaestroGroup/dgutils.git'

From a local checkout, use `python -m pip install '.[notebook]'` instead.
`savehtml.save()` uses nbconvert from the active Python environment and writes
changed notebooks directly into `html/`. Conversion failures raise an exception.
The core package can be imported without IPython or nbconvert installed.

## POV-Ray

Install POV-Ray separately. `pypov.pov_run()` finds `povray` on `PATH`, with
`~/local/bin/povray` as a fallback. You can also select an executable explicitly:

```python
from dgutils import pypov

pypov.pov_run('scene.pov', executable='/opt/local/bin/povray')
```

POV-Ray uses its normal configuration discovery unless you pass
`ini_file='/path/to/povray.ini'`. A missing home-directory INI file is no longer
forced onto the command line. Failed renders raise an exception before cropping.
Existing quality options are preserved: explicit width and height apply when
`res='high'`; low quality uses the renderer's configuration.

## Compatibility checks

From the checkout, run:

    MPLBACKEND=Agg python -m unittest discover -s tests -v

The tests cover colormap names, `None`, and colormap objects; simulated legacy
Matplotlib APIs; signed and fractional Lab colors; font cache refresh; plot
rendering; notebook export; and POV-Ray command construction and image cropping.
Notebook integration tests require the `notebook` extra. The POV-Ray unit tests
do not require an installed renderer.

Verified with Python 3.13.18, NumPy 2.5.5, Matplotlib 3.11.2, SciPy 1.18.1,
Pillow 13.0.0, IPython 9.18.1, and nbconvert 7.17.2. Legacy API paths are tested
with simulations, not separate installations of older Matplotlib releases.
