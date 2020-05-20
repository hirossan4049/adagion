

import mss
import cv2
import numpy




class RealtimeRecode:
    pass

class Recode:
    def __init__(self,filename,time,fps=30):
        self.filename = filename
        self.time = time
        self.fps = fps


class Sct_loop:
    def __init__(self,quality=2):
        self.res = [0, b""]
        self._back_res = b""
        self.sct = mss.mss()
        self.quality = quality
        self.do_run = True
        # FIXME: 画面サイズを取得してやる。
        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1200}
        self.width = self.monitor["width"] * 2
        self.height = self.monitor["height"] * 2
        self._fps_cache = 0
        self._draw_num = 0
        self._draw_cache_num = 0
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 25]

    def sct_func(self):
        sct_mss = self.sct.grab(self.monitor)
        img = numpy.array(sct_mss)

        return img

    def sct_mainloop(self):
        with concurrent.futures.ThreadPoolExecutor() as excuter:
            while self.do_run:
                future = excuter.submit(self.sct_func)
                time.sleep(1/30)


if __name__ == "__main__":
    sct = Sct_loop()
    print("RUN")
    print(sct.sct_func())
