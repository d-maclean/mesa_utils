# Module to provide utility functions for MESA; primarily related to loading and formatting files
# D. Maclean 2023 GNU GPL or smth idk
import os
import glob
import numpy as np
from matplotlib import pyplot as plt
import mesa_reader as mr
from .hr_diagram import *

## Get history files
def load_dir_history(dir: str, ext: str = 'data') -> tuple[list,list]:
    '''
    Loads all MESA history files from `dir`.
    - Pass `ext` to specify the MESA history file extension; defaults to `data`.    
    Returns a tuple of format `(list[history], list[labels])`
    '''
    files = glob.glob(os.path.join(dir, f'*.{ext}'))


    history = np.empty(len(files), dtype=object)
    labels = np.empty(len(files), dtype=str)

    for i, f in enumerate(files):
        _data = mr.MesaData(f)
        _name = os.path.split(f)[1]
        history[i] = _data
        labels[i] = _name
    
    return (history, labels)


def load_grid_history(dir: str,
                     history_name: str = 'history.data', folders_dir: str = 'folders', logs_dir: str = 'LOGS') -> tuple[list,list]:
    '''
    Loads MESA history files named `history_name` from a grid directory structure located at `dir.`
    
    Returns a tuple of format `(list[history], list[labels])`.
    '''
    search_path = os.path.join(dir, folders_dir, '*', logs_dir, history_name)
    files = glob.glob(search_path)
    
    history = np.empty(len(files), dtype=object)
    labels = np.empty(len(files), dtype=str)

    for i, f in enumerate(files):
        _data = mr.MesaData(f)
        LOGS_dir = os.path.split(f)[0]
        star_dir = os.path.split(LOGS_dir)[0]
        _name = star_dir.split(os.sep)[-1]

        history[i] = _data
        labels[i] = _name
    
    return (history, labels)


def history_dict(history: list, names: list) -> dict:
    '''Returns a dictionary with values of `history` and keys given by `names`.'''
    _output = {}
    for i, sec in enumerate(history):
        _output[names[i]] = sec
    return _output


class GridData():
    '''
    Container class for visualization of MESA grids containing multiple history files.
    
    - `path` points to the directory containing the star folders.
    - `from_dir` should be passed as `True` if you wish to load a folder full of history files, rather than a true "grid." 
    '''
    def __init__(self, path: str,
                 from_dir: bool = False, history_name: str = 'history.data', logs_dir: str = 'LOGS'):
        if from_dir == True:
            self.data = load_dir_history(path)
        else:
            self.data = load_grid_history(dir= path, history_name=history_name, logs_dir=logs_dir)
            
        self.labels = sorted(self.data[1], key= lambda x: x)
        self.stars = sorted(self.data[0], key=lambda x: x.star_mass[0])        
        
        return
    
    def color_palette(self, palette: list):
        self.colors = palette
        
        return
    
    def make_labels(self):
        '''Creates an array of labels called `cleaned_labels` from the stars' initial masses. May be useful.'''
        self.cleaned_labels = [f'{x.star_mass[0]:.2f}' for x in self.stars]

        return


