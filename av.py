import pyaudio
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
    sample_rate = 44100  # 44.1kHz sampling rate
    chunk = 4096  # 2^12 samples for buffer
    record_secs = 3  # seconds to record
    dev_index = 2  # device index found by p.get_device_info_by_index(ii)

    def __init__(self, path):
        self.path = path
        self.audio = None
        self.stream = None
        self.frames = None

    def start(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.form_1,
            rate=self.sample_rate,
            channels=self.channels,
            input_device_index=self.dev_index,
            input=True,
            frames_per_buffer=self.chunk
        )
        self.frames = []
        for ii in range(0, int((self.sample_rate / self.chunk) * self.record_secs)):
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        wavefile = wave.open(self.path, 'wb')
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self.audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.sample_rate)
        wavefile.writeframes(b''.join(self.frames))
        wavefile.close()
