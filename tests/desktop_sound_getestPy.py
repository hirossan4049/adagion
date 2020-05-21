from os.path import basename

import pyaudio
import numpy as np
import scipy.io.wavfile

RATE = 12000


def record_audio(output_name):
    CHUNK = 1024
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1

    pa = pyaudio.PyAudio()
    stream = pa.open(rate=RATE,
                     channels=CHANNELS,
                     format=FORMAT,
                     input=True,
                     frames_per_buffer=CHUNK,
                     input_device_index=0)

    print("RECORD START")
    print("ctrl-C : STOP RECORDING")

    # RECORDING ###############
    # Stop with Ctrl-C
    frame = []
    while True:
        try:
            # Record
            d = stream.read(CHUNK)
            d = np.frombuffer(d, dtype=np.float32)  # convert numpy
            frame.append(d)

        except KeyboardInterrupt:
            # Ctrl - c  
            break
    # END # RECORDING ###############

    # CLOSE
    stream.stop_stream()
    stream.close()
    pa.terminate()

    # Numpy Array
    frame = np.array(frame).flatten()
    print("STOP {} samples  {:.2f}s".format(frame.size, frame.size / RATE))
    # Write Wavfile with scipy module
    scipy.io.wavfile.write(output_name, RATE, frame)
    print("OUTPUT: {}".format(basename(output_name)))


record_audio("test.wav")
