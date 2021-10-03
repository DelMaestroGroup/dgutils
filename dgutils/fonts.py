# Helper utilties for dealing with local fonts in matplotlib

import matplotlib as mpl
import matplotlib.font_manager as fm
import os

def set_custom_font(font_path, name='custom', labelweight='light'):
    '''Set a custom font to be used for plotting in matplotlib.
       font_path : the full path to a .ttf font file.
    '''
    
    if os.path.isfile(font_path):
        fe = fm.FontEntry(fname=font_path,name=name)
        fm.fontManager.ttflist.insert(0, fe) 

        mpl.rcParams['font.family'] = fe.name
        mpl.rcParams['mathtext.fontset'] = 'custom'
        mpl.rcParams['mathtext.rm'] = f'{fe.name}:regular'
        mpl.rcParams['mathtext.it'] = f'{fe.name}:italic'
        mpl.rcParams['mathtext.bf'] = f'{fe.name}:bold'
        mpl.rcParams['mathtext.sf'] = f'{fe.name}:sans'
        mpl.rcParams['mathtext.tt'] = f'{fe.name}:monospace'
        mpl.rcParams['axes.labelweight'] = labelweight
        mpl.rcParams['font.sans-serif'] = fe.name
    else:
        print(f'Font: {font_path} not found\n')
