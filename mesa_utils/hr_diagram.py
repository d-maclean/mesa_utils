from matplotlib.collections import LineCollection
from collections import namedtuple
from matplotlib import pyplot as plt
from matplotlib import colors as c
import mesa_reader as mr
import numpy as np

def make_hr_args(axis, title: str = 'HR Diagram'):
    '''Takes a pyplot axis `axis` and formats it for an HR diagram.'''
    axis.invert_xaxis()
    axis.set_title(title)
    axis.set_xlabel(r'log $T_{eff}$ $(K)$')
    axis.set_ylabel(r'log L $(L_{sun})$')
    return

# original function by Poojan Agrawal; adapted by Duncan Maclean

def plot_HR_z(star: mr.MesaData,
                     z: str,
                     ax =None, 
                     cmap=None, 
                     cmap_label = None,
                     zmin=None,
                     zmax =None,
                     lim_z = False,
                     decorate_plot= True, 
                     mass_as_text = False,
                     
                     LogNorm = False):
        '''Plot an HR diagram using `star`'s history, colored dynamically with the `z` array.'''
        # read the file based on the filepath  # I just plug in a mr.MesaData instance      
        # grab columns for y = log_L, x= log_Teff and whatever z is
        
        y = star.log_L
        x = star.log_Teff
        
        z = star.data(z)
        
        # if no axis is passed, make a new plot
        if ax is None:
            fig = plt.figure()
        ax = ax or plt.gca()
    
        # define a colormap; default is plasma_r
        if cmap is None:
            cmap = 'plasma_r'
        else:
            cmap = plt.get_cmap(cmap)
            
        # get limits for the colorbar/z
        if zmin is None:
            if lim_z:
                zmin = 0.0
            else:
                zmin = z.min()
        if zmax is None:
            if lim_z:
                zmax = 1.0
            else:
                zmax = z.max()
                
        # set the segments based on x and y values
        points = np.array([x,y]).T.reshape(-1,1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # define the norm (logNormal or simple normal)
        if LogNorm:
            norm = c.LogNorm(zmin, zmax)
        else:
            norm = plt.Normalize(zmin, zmax)
        
        # color and plot the segments based on z
        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(z)
        line = ax.add_collection(lc)
        ax.autoscale()
        
        # additional stuff
        #if mass_as_text:
        #    tx = self.log_Teff.iloc[0] + 0.1
        #    ty = self.log_L.iloc[0] -0.01
        #    ax.text(tx,ty,r"%.1f$\,{\rm M_\odot}$" %self.ini_mass,size = 8)
        if decorate_plot:    
            bar = plt.colorbar(line)
            bar.set_label(cmap_label)
            
            ax.set_xlabel('log[Teff/K]')
            ax.set_ylabel('log[L/L$_\odot$]')
            ax.invert_xaxis()
            
        HRD = namedtuple('HRD', 'line')

        return HRD(line)