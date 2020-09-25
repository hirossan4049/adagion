import pyaudio
import subprocess
import threading
import time

#class FrameObserver:
#    def __init__(self):
#        self.frame = b''
#
#    @property
#    def frame(self):
#        pass
#
#    @property.setter
#    def frame(self,frame):
#        self.frame = frame
        


class RealtimeAudioRecorder:
    def __init__(self,CHANNELS=2, RATE=44100):
        self.now_outplayer = subprocess.check_output(['lib/AudioSwitcher','-c']).decode().replace('\n','')
        self.blackhole_name = "BlackHole 16ch"

        self.p = pyaudio.PyAudio()

        self.devices = self.devices()
        self.outplayer_index = self.devices.get(self.now_outplayer)
        self.blackhole_index = self.devices.get(self.blackhole_name)

        self.frame_index = 0
        self._cashe_frame_index = None

        self.data = b''
        self._recode_thread = None
        self.isRecording = False

        if self.blackhole_index is None:
            raise Exception("BlackHole not found")

        self.CHUNK = 1024
        FORMAT = pyaudio.paInt16 # int16型
        #CHANNELS = 2             # ステレオ
        #RATE = 44100             # 441.kHz

        self.stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK,
                        input_device_index=self.blackhole_index
                        )
        self.stream_out = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=self.CHUNK,
                        output_device_index=self.outplayer_index
                        )


    def devices(self):
    # detect devices:
        host_info = self.p.get_host_api_info_by_index(0)    
        device_count = host_info.get('deviceCount')
        devices = {}
        # iterate betweeNn devices:
        for i in range(0, device_count):
            device = self.p.get_device_info_by_host_api_device_index(0, i)
            devices[device['name']] = device['index']

        return devices

    def _loop_recoding(self,*args):
        while self.isRecording:
            data = self.stream.read(self.CHUNK)
            self.stream_out.write(data)
            self.data = data
            self.frame_index += 1


    def start(self):
        subprocess.check_output(['lib/AudioSwitcher','-s',self.blackhole_name]).decode().replace('\n','')
        self.isRecording = True
        threading.Thread(target=self._loop_recoding).start()
        #self._recode_thread.start()
    # FIXME
    def get(self):
        if self.frame_index == self._cashe_frame_index:
            while True:
                if self.frame_index != self._cashe_frame_index:
                    break
                #time.sleep(1/200)
        self._cashe_frame_index = self.frame_index
        return self.data

    def get_once(self):
        self.start()
        res = self.get()
        self.stop()
        return res

    def stop(self):
        subprocess.check_output(['lib/AudioSwitcher','-s',self.now_outplayer]).decode().replace('\n','')
        self.isRecording = False
