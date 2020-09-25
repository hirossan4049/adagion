import tempfile
import time
import threading
import asyncio
#from multiprocessing import Pool, Process
from pathos.pools import _ProcessPool as Pool
#from pathos.pools import ProcessPool as Pool
import mss
import cv2
#import skvideo.io
import numpy
import concurrent.futures

import imageio

#from moviepy.editor import VideoFileClip
from ffmpy3 import FFmpeg

from audioRecoder import AudioRecoder


class RealtimeRecorder:
    def __init__(self):
        self.sct_mss = mss.mss()
        # FIXME:
        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1200}
        #self.width = self.monitor["width"] * 2
        #self.height = self.monitor["height"] * 2
        #self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 25]

    def sct(self):
        sct_mss = self.sct_mss.grab(self.monitor)
        img = numpy.array(sct_mss)
        return img


# TODO:デスクトップ音声ってどうやって取得するん
class Recorder:
    def __init__(self,filename,time,*,fps=30,desktop_sound=False,):
        self.filename = filename
        self.filext = filename.split('.')[-1]
        self.time = time
        self.fps = fps
        self.isRecoding = False
        self.desktop_sound = desktop_sound
        self.r_record = RealtimeRecorder()
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 25]
        self.tempfolder = tempfile.TemporaryDirectory()
        #cv2.setNumThreads(0)

    def _recorder(self):
        print("recoder called!")
        frame = self.r_record.sct()
        return frame

    def _frame_record(self):
        t = time.time()
        frame = self._recorder()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        endtime = time.time() - t
        
        self.writer.append_data(frame)
        #print(f"fps: {1 / endtime}")
        #time.sleep(0.2 - endtime)
        #self.writer.writeFrame(frame)
        #self.writer.append_data(frame)
        #threading.Thread(target=self._frame_writer,args=(frame,)).start()

    def _frame_writer(self,frame):
        self.writer.append_data(frame)

    def _record_audio(self,filename):
        ar = AudioRecoder(filename,None)
        threading.Thread(target=ar.start).start()
        return ar


    def test(self):
        print("TESTING...")

    def start_record(self):
        #writer = skvideo.io.FFmpegWriter("outputvideo.mp4")
        fps = 30
        width = 3840
        height = 2400
        crf = 17
        #self.writer = skvideo.io.FFmpegWriter('test_ffmpeg.mp4', 
        #            inputdict={'-r': str(fps), '-s':'{}x{}'.format(width,height)},
        #            outputdict={'-r': str(fps), '-c:v': 'libx264', '-crf': str(crf), '-preset': 'ultrafast', '-pix_fmt': 'yuv444p'}
        #) 
        tempvfile = self.tempfolder.name + "/v." + self.filext
        self.writer = imageio.get_writer(tempvfile,fps=10)

        print(self.writer)
        #print(sct.shape)
        print("record start")
        threading.Thread(target=self._timekeeper).start()

        if self.desktop_sound:
            audiofile = self.tempfolder.name + "/a.wav"
            ar = self._record_audio(audiofile)

        # FIXME: Threadだと10fpsぐらいだと間に合うが、20fps 超えると無理。
        with concurrent.futures.ThreadPoolExecutor() as excuter:
            while self.isRecoding:
                t = time.time()
                future = excuter.submit(self._frame_record)
                print("fps: {}".format(time.time() - t))
                time.sleep(1/10)

        if self.desktop_sound:
            ar.stop()
        # FIXME; process run
        #excuter = concurrent.futures.ProcessPoolExecutor(max_workers=10)
        #while self.isRecoding:
        #    res = excuter.map(self._frame_record,range(1))
        #    print(res)
        #    time.sleep(1/10)
        #frame = 0
        #kwhile self.isRecoding:
        #    threading.Thread(target=self._frame_record).start()
        #    frame += 1
        #    time.sleep(1/20)
        #Jprint(frame)
        #p = Pool(4)
        #while self.isRecoding:
        #    #p.apply(self._test)
        #    #res = p.apply_async(self.test)
        #    res = p.map(self._frame_record,range(1))
        #    time.sleep(1/60)

        #p.close()
        #excuter.close()
        #while self.isRecoding:
        #    self._frame_record()
            #time.sleep(1/60)

        print("closeing")
        time.sleep(1)
        self.writer.close()

        if self.desktop_sound:
            print('enable desktop_sound')
            ff = FFmpeg(inputs={tempvfile: None, audiofile: None},
                        outputs={self.filename: '-c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -loglevel quiet'})
            ff.run()
        

    def _timekeeper(self):
        self.isRecoding = True
        print("time keep start",self.time)
        time.sleep(self.time)
        self.isRecoding = False
        print("time keep end")

    #def sct_mainloop(self):
    #    with concurrent.futures.ThreadPoolExecutor() as excuter:
    #        while self.isRecoding:
    #            future = excuter.submit(self._frame_recode)
    #            time.sleep(1/30)
    #    print("closeing")
    #    time.sleep(1)
    #    self.writer.close()


    #def opencv_recode(self):
        #size = (3840,2400) 
        #fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') 
        ##fmt = cv2.VideoWriter_fourcc(*'MJPG') 
        #writer = cv2.VideoWriter('outtest.mp4', fmt, 10, size) 

        ##writer.write(frame) # 画像を1フレーム分として書き込み
        #for i in range(10):
        #    sct = self._recode()
        #    #_, jpeg = cv2.imencode('.jpg', sct, self.encode_param)
        #    #print(sct.shape)
        #    #cv2.imwrite("images/test_{}.png".format(str(i)),sct)
        #    writer.write(sct)
        #    time.sleep(1)
        #writer.release() 




if __name__ == "__main__":
    sct = Recorder("test12345.mp4",10, desktop_sound=True)
    sct.start_record()
