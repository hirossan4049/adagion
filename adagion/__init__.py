import time

import mss
import cv2
import skvideo.io
import numpy




class RealtimeRecode:
    def __init__(self):
        self.sct_mss = mss.mss()
        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1200}
        #self.width = self.monitor["width"] * 2
        #self.height = self.monitor["height"] * 2
        #self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 25]

    def sct(self):
        sct_mss = self.sct_mss.grab(self.monitor)
        img = numpy.array(sct_mss)
        return img


# TODO:デスクトップ音声ってどうやって取得するん
class Recode:
    def __init__(self,filename,time,fps=30):
        self.filename = filename
        self.time = time
        self.fps = fps
        self.isRecoding = False
        self.r_recode = RealtimeRecode()

    def _recode(self):
        frame = self.r_recode.sct()
        return frame

    def start_recode(self):
        #size = (3840,2400) 
        #fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') 
        ##fmt = cv2.VideoWriter_fourcc(*'MJPG') 
        #writer = cv2.VideoWriter('outtest.avi', fmt, 1, size) 

        ##writer.write(frame) # 画像を1フレーム分として書き込み
        #for i in range(10):
        #    sct = self._recode()
        #    #cv2.imwrite("images/test_{}.png".format(str(i)),sct)
        #    writer.write(sct) 

        #writer.release() # ファイルを閉じる
        writer = skvideo.io.FFmpegWriter("outputvideo.mp4")
        sct = self._recode()
        for i in range(5):
                writer.writeFrame(sct)
        writer.close()

    def _timekeeper(self):
        self.isRecoding = True
        time.sleep(self.time)
        self.isRecoding = False



#
#    def sct_mainloop(self):
#        with concurrent.futures.ThreadPoolExecutor() as excuter:
#            while self.do_run:
#                future = excuter.submit(self.sct_func)
#                time.sleep(1/30)


if __name__ == "__main__":
    sct = Recode("test.mp4",30)
    sct.start_recode()
