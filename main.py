#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True) 
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('gradients_generated.pdf')

def hsv2rgb(h, s, v):
    #TODO
    if s == 0:
        return(v, v, v)

    hs = int(h/60)
    r = (h/60)-hs
    hs %= 6
    x = v*(1-s)
    y = v*(1-s*r)
    z = v*(1-s*(1-r))

    if hs == 0:
        h = v
        s = z
        v = x

    if hs == 1:
        h = y
        s = v
        v = x

    if hs == 2:
        h = x
        s = v
        v = z

    if hs == 3:
        h = x
        s = y

    if hs == 4:
        h = z
        s = x

    if hs == 5:
        h = v
        s = x
        v = y

    return (h, s, v)

def gradient_rgb_bw(v):
    #TODO
    return (v, v, v)


def gradient_rgb_gbr(v):
    #TODO
    if v<1/2:
        r = 0
        g = 1-(2*v)
        b = 2*v
    else:
        r = 2*v-1
        g = 0
        b = 2-2*v

    return (r, g, b)


def gradient_rgb_gbr_full(v):
    #TODO

    if v<1/4:
        r = 0
        g = 1
        b = 4*v
    elif v<1/2:
        r = 0
        g = 2-4*v
        b = 1
    elif v<3/4:
        r = 4*v-2
        g = 0
        b = 1
    else:
        r = 1
        g = 0
        b = 4-4*v
    return (r, g, b)


def gradient_rgb_wb_custom(v):
    #TODO
    if v<1/7:
        r = 1
        g = 1-7*v
        b = 1
    elif v<2/7:
        r = 2-7*v
        g = 0
        b = 1
    elif v<3/7:
        r = 0
        g = 7*v-2
        b = 1
    elif v<4/7:
        r = 0
        g = 1
        b = 4-7*v
    elif v<5/7:
        r = 7*v-4
        g = 1
        b = 0
    elif v<6/7:
        r = 1
        g = 6-7*v
        b = 0
    else:
        r = 7-7*v
        g = 0
        b = 0
    return (r, g, b)


def gradient_hsv_bw(v):
    #TODO
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    #TODO
    return hsv2rgb(120+(v*240), 1, 1)

def gradient_hsv_unknown(v):
    #TODO
    return hsv2rgb(120-(v*120), 1/2, 1)


def gradient_hsv_custom(v):
    #TODO
    if v>0.5:
        v = np.fabs(v-1)
    return hsv2rgb(120+720*v, np.fabs(0.7-1.4*v)+0.3, 1)
    #return hsv2rgb(360*v, 1-v, 1)

if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
