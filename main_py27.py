from __future__ import print_function

import sys
from PIL import Image
from StringIO import StringIO

import twain
# from pyScanLib import pyScanLib

from maps import *

def print_cap(cap, stream=sys.stdout):
    try:
        tmp = src.GetCapability(cap)
        print('{:<4}  {:<24}  {}'.format(cap, cap_map[cap], tmp), file=stream)
    except Exception as e:
        print(e, file=sys.stderr)

def print_cap_default(cap):
    print(str(src.GetCapabilityDefault(cap)))

def print_cap_curr(cap):
    print(str(src.GetCapabilityCurrent(cap)))

print_sep = '=================='

def capabilities():

    # print(print_sep)
    #
    # print_cap(twain.ICAP_XRESOLUTION)
    # print_cap(twain.ICAP_YRESOLUTION)
    # print_cap(twain.ICAP_XSCALING)
    # print_cap(twain.ICAP_YSCALING)
    # print_cap(twain.ICAP_XNATIVERESOLUTION)
    # print_cap(twain.ICAP_YNATIVERESOLUTION)
    # print_cap(twain.ICAP_PHYSICALHEIGHT)
    # print_cap(twain.ICAP_PHYSICALWIDTH)
    #
    # print(print_sep)
    #
    # print_cap(twain.ICAP_PIXELTYPE)
    # print_cap_default(twain.ICAP_PIXELTYPE)
    # src.SetCapability(twain.ICAP_PIXELTYPE, twain.TWTY_UINT16, twain.TWPT_BW)
    # print_cap_curr(twain.ICAP_PIXELTYPE)
    # print_cap(twain.ICAP_PIXELTYPE)
    #
    # print(print_sep)
    #
    # src.SetCapability(twain.ICAP_BRIGHTNESS, twain.TWTY_FIX32,0.0)
    # print_cap(twain.ICAP_BRIGHTNESS)
    # print_cap(twain.ICAP_CONTRAST)
    # # print_cap(twain.ICAP_HIGHLIGHT)
    # # print_cap(twain.ICAP_SHADOW)
    #
    # print(print_sep)
    #
    # set_dpi(300)
    # # src.SetCapability(twain.ICAP_UNITS, twain.TWTY_UINT16, twain.TWUN_CENTIMETERS)
    # # src.SetCapability(twain.ICAP_UNITS, twain.TWTY_UINT16, twain.TWUN_PIXELS)

    supported_caps = src.GetCapability(twain.CAP_SUPPORTEDCAPS)[1][2]

    out = open(src.GetSourceName() + '.txt', 'w')


    for cap in supported_caps:
        print_cap(cap, out)

def set_dpi(dpi):
    src.SetCapability(
        twain.ICAP_XRESOLUTION, twain.TWTY_FIX32, float(dpi))
    src.SetCapability(
        twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, float(dpi))


def scan():
    src.RequestAcquire(0, 1)
    print(src.GetImageInfo())

    handle = src.XferImageNatively()[0]
    bm = twain.DIBToBMFile(handle)
    twain.GlobalHandleFree(handle)
    img = Image.open(StringIO(bm))
    return img


if __name__ == '__main__':

    sm = twain.SourceManager(0)
    src_lst = sm.GetSourceList()
    print(src_lst, file=sys.stderr)
    src = sm.OpenSource(src_lst[0])
    print(print_sep)

    # capabilities()
    # print(src.GetImageLayout())

    set_dpi(150)

    # Set scan size to A4 paper
    src.SetCapability(twain.ICAP_SUPPORTEDSIZES, twain.TWTY_UINT16, twain.TWSS_A4)
    # src.SetImageLayout((0.0, 0.0, 8.267, 11.693), 1, 1, 1)

    img = scan()
    img.show()

    src.destroy()
    sm.destroy()