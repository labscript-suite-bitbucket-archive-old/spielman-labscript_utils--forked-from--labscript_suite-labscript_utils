# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 09:16:29 2015

@author: Ian Spielman

Contains simple utilities that many functions can call
"""

from __future__ import division, print_function 
import matplotlib.pyplot as plt 
from cStringIO import StringIO 
from time import sleep 
from PIL import Image 
import win32clipboard 
import numpy as np 
 
# TODO import to pillow? 
# TODO crop around axis 
 
def copy2clipboard(fig=None, resize=1, pix_around=5): 
    print(type(fig)) 
    if not fig: 
        fig = plt.gcf() 
        ax = plt.gca() 
    else: 
        ax = fig.axes[0] 
 
    fig.set_facecolor('white') 
 
    output = StringIO() 
    fig.canvas.draw() 
    buf = fig.canvas.buffer_rgba() 
    size = fig.canvas.size() 
    w, h = size.width(), size.height() 
    im = Image.frombuffer('RGBA', (w, h), buf, 'raw', 'RGBA', 0, 1) 
 
    # crop canvas and give it some breathing space 
    crop_size = np.array(ax.get_tightbbox(fig.canvas.renderer).bounds, dtype=int) 
    crop_size[2:] += crop_size[:2] 
    crop_size[:2] -= pix_around 
    crop_size[2:] += 2*pix_around 
    crop_size[crop_size < 0] = 0 
    # TODO correct croping 
 
    # now resize cropped image respecting aspect_ratio 
    aspect_ratio = w*1.0/h 
    new_size = (crop_size[2:]*np.array([1, aspect_ratio])*resize).astype(int) 
 
    im.convert('RGB').crop(crop_size).resize(new_size, Image.LANCZOS).save(output, 'BMP') 
    data = output.getvalue()[14:]  # drop BMP header 
    output.close() 
 
    try: 
        win32clipboard.OpenClipboard() 
        win32clipboard.EmptyClipboard() 
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data) 
        win32clipboard.CloseClipboard() 
    except: 
        sleep(0.2) 
        copy2clipboard(fig) 

def ValidName(name, RaiseError=False):
    try:
        # Test that name is a valid Python variable name:
        exec '%s = None'%name
        assert '.' not in name
    except:
        if RaiseError:
            raise ValueError('%s is not a valid Python variable name.'%name)

        return False
    return True

