# Changelog

All notable changes to the `dgutils` library  are documented in this file.

## 0.4.5 (2026-11-16)

- Replace the removed Matplotlib `cm.get_cmap()` call with feature detection of
  `colormaps.get_cmap()`, retaining the legacy fallback and support for names,
  `None`, and `Colormap` instances.
- Store Lab values as floating point. Unsigned storage was a preexisting bug
  that discarded signs and fractions and now raises with current NumPy.
  Correcting it can change the nearest color returned by `get_color_name_lab()`;
  the palette and distance weighting are unchanged.
- Use the public legend-title accessor in `colorize_plot()` as a preventive
  compatibility fix; the former private attribute still worked during testing.
- Refresh cached font lookups after custom registration, fixing an existing
  stale-cache bug while preserving custom aliases and registration priority.
- Discover POV-Ray on `PATH` with the legacy executable fallback, add optional
  `executable` and `ini_file` keyword arguments, and use normal configuration
  discovery by default. Propagate failed renders before attempting cropping.
  These address existing machine-specific paths and error handling, not a
  removed Python or Pillow API.
- Run HTML exports with the active Python environment's nbconvert, write directly
  to `html/`, and propagate conversion failures. This fixes existing PATH and
  portability problems; `--to html` remains supported.
- Declare the optional `notebook` extra and defer IPython imports until a notebook
  banner is requested. Existing core dependencies and Python minimum are retained;
  SciPy is currently unused but has not been removed from dependency metadata.
- Add targeted unittest coverage, including real plot rendering and notebook
  exports. Actual rendering with the installed POV-Ray could not be verified in
  the test session because even `--version` stalled with macOS service errors.

### Additional fixes for preexisting helper bugs

- Return all requested samples from `pypov.generate_linear_path()`, including
  both endpoints for two or more points. Zero points returns an empty list;
  one point returns the start. Negative and non-integer counts raise errors.
- Fix `pypov.Vector.__repr__()` for tuple-backed and empty vectors.
- Fix `Item` indexing and assignment across arguments followed by options,
  including negative indices and bounds errors. Copy options into a mutable
  list so subclass options can be replaced without sharing caller storage.
- Detect RGB scale from all three channels in `colors.rgb_to_hex()`, fixing
  normalized red/white endpoints and byte colors whose red component is zero.
  Inputs whose RGB channels are all at most 1 default to normalized; use the
  new `full=True` argument for ambiguous low byte values such as `(1, 0, 0)`,
  or `full=False` to explicitly select normalized values. Existing truncation
  and ignored-alpha behavior are preserved; narrow NumPy integers no longer
  overflow during scaling.
- Add regression tests for these helper fixes.

## 0.4.4 (2026-09-11)
- fixed a font bug related to sans serif

## 0.4.3 (2026-05-16)
- added `nb.py` with some simple scripts to improve notebooks

## 0.3.9 (2023-08-01)
- added ability to auto-crop image via "auto_crop" option; default is no

## 0.3.8 (2023-08-01)
- Updated pypov with new get_color functionality
- added image_map class

## 0.3.7 (2022-09-08)
- added structure to iterate over axes when colorizing, not yet implemented

## 0.3.6 (2022-02-05)
- updated dependencies

## 0.3.5 (2022-01-03)
- added a new font properties object getter

## 0.3.4 (2021-12-03)
- updated `savehtml.py` to reflect changed command line options for nbconvert 

## 0.2.5 (2021-08-04)
- added a new function `colorize_plot` to change the color of all components in
  matplotlib plot

## 0.1.0 (2020-06-20)

- initial upload to github
- started adding tools

