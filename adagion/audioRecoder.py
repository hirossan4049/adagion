import threading
import time

import pyaudio
import wave

from realtimeAudioRecoder import RealtimeAudioRecorder

class AudioRecoder:
    def __init__(self,filename,time,CHANNELS=2,RATE=44100):
        ext = filename.split('.')[-1]
        if ext != "wav":
            raise Exception(f"{ext} is not supported. use .wav")

        self.rar = RealtimeAudioRecorder(CHANNELS=CHANNELS)
        self.CHANNELS = CHANNELS
        self.RATE = RATE
        self.filename = filename
        self.time = time
        self.isStopIDK = True if self.time is None else False
        self.isRecording = False
        print('is Stop IDK',self.isStopIDK)



    def start(self):
        wf = wave.open(self.filename,'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(self.RATE)

        threading.Thread(target=self.rar.start).start()
        if self.isStopIDK:
            self.isRecoding = True
        else:
            threading.Thread(target=self._timekeeper).start()
        while self.isRecoding:
            #frame = self.rar.get()
            data = self.rar.stream.read(self.rar.CHUNK)
            self.rar.stream_out.write(data)
            wf.writeframes(data)
       # wf.writeframes(b''.join(frames))

        wf.close()
        self.rar.stop()

    def stop(self):
        self.isRecoding = False

    def _timekeeper(self):
        self.isRecoding = True
        time.sleep(self.time)
        self.isRecoding = False
        

if __name__ == "__main__":
    ar = AudioRecoder("tester.wav",None)
    threading.Thread(target=ar.start).start()
    time.sleep(5)
    ar.stop()
