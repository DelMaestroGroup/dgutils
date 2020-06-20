'''
savehtml.py

Export Jupyter notebooks as html files if the .ipynb has changed.
'''

import os
import datetime
import subprocess

def modified(filename):
    '''Get the modification time of a file. '''
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def save():
    ''' Save all Jupyter notebooks as html files. '''

    # Check if we an html output directory, if not, make it
    if not os.path.isdir('html'):
        os.mkdir('html')

    # Get the list of all notebooks
    notebooks = [f for f in os.listdir('.') if os.path.isfile(f)]

    # keep only the .ipynb files
    for notebook in notebooks:
        # get the name and extension
        name,extension = os.path.splitext(notebook)

        # check if we have a .ipynb file
        if extension == '.ipynb':

            # check if we need to regenerate the html file 
            html = name + '.html'
            if not os.path.isfile('html/%s'%html) or (modified(notebook) > modified('html/%s'%html)):
                subprocess.call(['jupyter','nbconvert',notebook])
                subprocess.call(['mv',html,'html/%s'%html])
                
