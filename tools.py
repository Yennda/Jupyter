import matplotlib
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
import math as m
import numpy as np
from copy import copy

from skimage import data, io, filters, util
import IPython

UMPX=87.3/1216

#useful functions
def derivation(V,i):
    #naivelly simple numerical derivation
    return V[i+1]-V[i]

def array_der(V):
    #derivation of an array
    dV=[]
    for i in range(len(V)-1):
        dV.append(derivation(V,i))
    dV.append(dV[-1])
    return dV

def split(m):
    #splits the list into two lists, one for indices, one for values, filters zero values
    x=[]
    y=[]
    for i in range(len(m)):
        if m[i]!=0:
            x.append(i)
            y.append(m[i])
    return [x, y]

def widths(sw):
    #returns widths and distances in pixels from the list in the form of the splitted list (function 'split')
    w=[]
    d=[]
    start=sw[0]
    for i in range(len(sw)-1):
        if sw[i]!=sw[i+1]-1:
            w.append(sw[i]-start)
            d.append(sw[i+1]-sw[i])
            start=sw[i+1]
    w.append(sw[-1]-start)
    return w, d

def wires_analysis(area_color, display=True):
    #profile (average of values in x direction)
    area=rgb2gray(area_color)
    y=[]
    wires=[]
    gaps=[]
    for r in area:
        y.append(sum(r))

    #derivation
    dy=array_der(y)
    #identification of wires and gaps:
    for i in range(len(y)):
        if m.fabs(dy[i])<max(dy)*0.65:
            if y[i]< np.average(y):
                wires.append(y[i])
                gaps.append(0)

            else:
                gaps.append(y[i])
                wires.append(0)

        else:
            wires.append(0)
            gaps.append(0)

    #gaining the right form of the data using some functions
    s_wires=split(wires)[0]
    w_wires=widths(s_wires)[0]
    d_wires=widths(s_wires)[1]
    if display:
        print(w_wires)
        print(d_wires)

        print('average width: {:.3f} um'.format(np.average(w_wires)*UMPX))
        print('average distance: {:.3f} um'.format(np.average(d_wires)*UMPX))
        print('std width: {:.3f} um'.format(np.std(w_wires)*UMPX))
        print('std distance: {:.3f} um'.format(np.std(d_wires)*UMPX))

        print('together: {:.3f} um'.format(np.average(w_wires)/14+np.average(d_wires)*UMPX))

        #shows the recognized wires in red
        area_wires=copy(area_color)
        for i in s_wires:
            area_wires[i,:]=(255,0,0)

        plt.imshow(area_wires)
        plt.savefig('tmp/wires_red.png', dpi=200, bbox_inches='tight')

        #graph
        fig = plt.figure()
        ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])

        ax.grid(linestyle='--')   
        ax.plot(np.arange(len(y)), y, linewidth=2)
        ax.set_title('Intensity profile in the image')
        ax.set_xlabel('x direction [px]')
        ax.set_ylabel('intensity a.u.')

    # ax.plot(np.arange(len(dy)), dy, linewidth=2)
    # ax.plot(np.arange(len(wires)), wires, linewidth=2)
    # ax.scatter(split(gaps)[0], split(gaps)[1], linewidth=2)
    return w_wires, d_wires
 
'''
def wires_analysis(area_color):
    #profile (average of values in x direction)
    area=rgb2gray(area_color)
    y=[]
    wires=[]
    gaps=[]
    for r in area:
        y.append(sum(r))

    #derivation
    dy=f.array_der(y)
    #identification of wires and gaps:
    for i in range(len(y)):
        if m.fabs(dy[i])<max(dy)*0.65:
            if y[i]< np.average(y):
                wires.append(y[i])
                gaps.append(0)

            else:
                gaps.append(y[i])
                wires.append(0)

        else:
            wires.append(0)
            gaps.append(0)

    #gaining the right form of the data using some functions
    s_wires=f.split(wires)[0]
    w_wires=f.widths(s_wires)[0]
    d_wires=f.widths(s_wires)[1]

    print(w_wires)
    print(d_wires)

    print('average width: {:.3f} um'.format(np.average(w_wires)/14))
    print('average distance: {:.3f} um'.format(np.average(d_wires)/14))
    print('std width: {:.3f} um'.format(np.std(w_wires)/14))
    print('std distance: {:.3f} um'.format(np.std(d_wires)/14))

    print('together: {:.3f} um'.format(np.average(w_wires)/14+np.average(d_wires)/14))
    
    #shows the recognized wires in red
    area_wires=copy(area_color)
    for i in s_wires:
        area_wires[i,:]=(255,0,0)

    plt.imshow(area_wires)
    plt.savefig('wires_red.png', dpi=200, bbox_inches='tight')
    
    #graph
    fig = plt.figure()
    ax = fig.add_axes([0.2, 0.2, 0.7, 0.7])

    ax.grid(linestyle='--')   
    ax.plot(np.arange(len(y)), y, linewidth=2)
    ax.set_title('Intensity profile in the image')
    ax.set_xlabel('x direction [px]')
    ax.set_ylabel('intensity a.u.')

    # ax.plot(np.arange(len(dy)), dy, linewidth=2)
    # ax.plot(np.arange(len(wires)), wires, linewidth=2)
    # ax.scatter(split(gaps)[0], split(gaps)[1], linewidth=2)
'''