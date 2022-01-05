import sys
from PIL import Image
from io import BytesIO

import twain

from maps import cap_map

twain_32_dll_path = 'D:\\repos\\wlsc10th-info\\auto-scan\\twain_32.dll'

class Scan:

    def __init__(self):
        self.src_manager = twain.SourceManager(1, dsm_name=twain_32_dll_path)
        self.src = None
        self.dpi = 200

    def get_sources(self):
        return self.src_manager.source_list

    def set_source(self, idx):
        self.src = self.src_manager.open_source(self.src_manager.source_list[idx])

    def set_dpi(self, dpi):
        self.dpi = float(dpi)
        self.src.set_capability(
            twain.ICAP_XRESOLUTION, twain.TWTY_FIX32, self.dpi)
        self.src.set_capability(
            twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, self.dpi)

    def set_pixel_type(self, pixel_type):
        pixel_type_map = {
            'bw': twain.TWPT_BW,
            'gray': twain.TWPT_GRAY,
            'rgb': twain.TWPT_RGB
        }

        try:
            self.pixel_type = pixel_type_map[pixel_type]
        except:
            self.pixel_type = twain.TWPT_RGB

        self.src.set_capability(
            twain.ICAP_PIXELTYPE, twain.TWTY_UINT16, self.pixel_type)

    def set_image_layout(self, left, top, width, height):
        raise NotImplementedError

    def debug(self):
        print(self.src.name)
        print(self.src.identity)

    def scan(self):
        self.src.RequestAcquire(0, 1)
        print('Scanning...')
        print('Image info:', self.src.image_info)
        print('Image Layout:', self.src.get_image_layout())

        handle, count = self.src.xfer_image_natively()
        bm = twain.dib_to_bm_file(handle)
        twain.global_handle_free(handle)
        img = Image.open(BytesIO(bm))
        return img

    def close(self):
        if self.src:
            self.src.close()
        if self.src_manager:
            self.src_manager.close()

    def print_cap(self, cap, stream=sys.stdout):
        try:
            tmp = self.src.get_capability(cap)
            print('{:<4}  {:<24}  {}'.format(cap, cap_map[cap], tmp), file=stream)
        except Exception as e:
            print(e, file=sys.stderr)

    def print_cap_default(self, cap):
        print(self.src.get_capability_default(cap))

    def print_cap_curr(self, cap):
        print(self.src.GetCapabilityCurrent(cap))

    def write_capabilities(self):
        supported_caps = self.src.GetCapability(twain.CAP_SUPPORTEDCAPS)[1][2]
        out = open(self.src.name + '_2.txt', 'w')
        for cap in supported_caps:
            self.print_cap(cap, out)

if __name__ == '__main__':

    scan = Scan()
    print(scan.get_sources())
    scan.set_source(0)

    scan.set_pixel_type('gray')
    scan.set_dpi(200)

    # Set scan size to A4 paper
    scan.src.set_capability(twain.ICAP_SUPPORTEDSIZES, twain.TWTY_UINT16, twain.TWSS_A4)
    # scan.src.set_image_layout((0.0, 0.0, 8.267, 11.693), 1, 1, 1)

    img = scan.scan()
    img.show()
    # img.save('1.bmp')