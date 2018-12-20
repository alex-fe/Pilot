import pyaudio
import time
import wave
from picamera import PiCamera


class Camera(object):
    camera = PiCamera()

    def __init__(self, path):
        self.path = path

    def start(self):
        self.camera.start_recording(self.path)

    def stop(self):
        self.camera.stop_recording()


class Audio(object):
    form_1 = pyaudio.paInt16  # 16-bit resolution
    channels = 1  # 1 channel
    chunk = 8192

    def __init__(self, path):
        self.path = path
        self.audio = None
        self.stream = None
        self.counter = 0

    def setup(self):
        self.audio = pyaudio.PyAudio()
        for i in range(self.audio.get_device_count()):
            dev = self.audio.get_device_info_by_index(i)
            if dev['name'] == 'USB Audio Device':
                break
        self.sample_rate = (
            int(self.audio.get_device_info_by_index(i)['defaultSampleRate'])
        )

    def start(self):
        self.stream = self.audio.open(
            format=self.form_1,
            rate=self.sample_rate,
            channels=self.channels,
            input_device_index=self.dev_index,
            input=True,
            frames_per_buffer=self.chunk
        )
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        record_time = self.end_time - self.start_time
        frames = [
            self.stream.read(self.chunk) for _ in
            range(0, int((self.sample_rate / self.chunk) * record_time))
        ]
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        wavefile = wave.open(self.path, 'wb')
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self.audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.sample_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()
