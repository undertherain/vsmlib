from matplotlib.colors import Normalize
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from sklearn.metrics import pairwise_distances
import PIL

class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        #m=max(abs(vmin),abs(vmax))
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        m=max(abs(self.vmin),abs(self.vmax))
        x, y =[-m, self.midpoint, m], [0, 0.5, 1]
        #x, y = [-20, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
 
    
def plot_heat(ax,m,xlabels,ylabels):
    #norm = Normalize(-10,10,False)
    norm = MidpointNormalize(midpoint=0)
    ax.set_aspect('equal')
    plt.xticks(rotation=90)    
    ax.set_xticks(np.arange(m.shape[1])+0.5, minor=False)
    ax.set_yticks(np.arange(m.shape[0])+0.5, minor=False)
    ax.set_xticklabels(xlabels, minor=False)
    ax.set_yticklabels(ylabels, minor=False)
    for tic in ax.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
    for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
    #ax.set_frame_on(False)
    heatmap = plt.pcolor(np.array(m), norm=norm, cmap=mpl.cm.RdBu, edgecolors="black")    
#    heatmap = plt.pcolor(np.array(m), cmap=mpl.cm.RdBu, edgecolors="black")    
    #im = ax.imshow(np.array(m), norm=norm, cmap=plt.cm.seismic, interpolation='none')
#fig.colorbar(im)
    cb=plt.colorbar(heatmap,orientation='horizontal',shrink=1,aspect=40)
    #cb.fraction=0.1
    
def draw_features_and_similarity(mm,words_of_interest):
    rows,cols,xlabels=mm.filter_submatrix(words_of_interest,25)
    ax=plt.subplot(1,2,1)
    plot_heat(ax,cols,xlabels,words_of_interest)
    #plot_heat(ax,abs(m),numbered)
    ax=plt.subplot(1,2,2)
    t = 1-pairwise_distances(rows, metric="cosine")
    np.fill_diagonal(t,0)
    plot_heat(ax,t,words_of_interest,words_of_interest)
    #plt.savefig("m1.pdf")

def draw_features(mm,words_of_interest,num_features=20):
    rows,cols,xlabels=mm.filter_submatrix(words_of_interest,num_features)
    ax=plt.subplot()
    plot_heat(ax,cols,xlabels,words_of_interest)

def plotvectors(m):
    a=m.matrix[:1000].T
    #my_cm = mpl.cm.get_cmap('RdBu')
    my_cm = mpl.cm.get_cmap('RdBu')
    normed_data = (a - np.min(a)) / (np.max(a) - np.min(a))
    mapped_datau8 = (255 * my_cm(normed_data)).astype('uint8')
    im = PIL.Image.fromarray(np.uint8(mapped_datau8))
    return im