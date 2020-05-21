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
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 25]

    def _recode(self):
        frame = self.r_recode.sct()
        return frame

    def start_recode(self):
        size = (3840,2400) 
        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') 
        #fmt = cv2.VideoWriter_fourcc(*'MJPG') 
        writer = cv2.VideoWriter('outtest.mp4', fmt, 10, size) 

        #writer.write(frame) # 画像を1フレーム分として書き込み
        for i in range(50):
            sct = self._recode()
            _, jpeg = cv2.imencode('.jpg', sct, self.encode_param)
            #print(sct.shape)
            #cv2.imwrite("images/test_{}.png".format(str(i)),sct)
            writer.write(jpeg) 

        writer.release() # ファイルを閉じる

        #writer = skvideo.io.FFmpegWriter("outputvideo.mp4")
        #sct = self._recode()
        #cv2.imwrite("omg.png",sct)
        #sct = cv2.imread("omg.png")
        #print(sct.shape)
        #for i in range(500):
        #        writer.writeFrame(sct)
        #writer.close()

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
