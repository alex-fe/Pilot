import time
import Adafruit_ADS1x15


def now():
    return int(time.time() * 1000)


class HeartBeat(object):
    # initialization
    GAIN = 2 / 3.0
    CURENT_STATE = 0
    THRESH = 525  # mid point in the waveform
    P = 512  # P is the peak
    T = 512  # T is the trough
    STATE_CHANGED = 0
    SAMPLE_COUNTER = 0
    LAST_BEAT_TIME = 0
    FIRST_BEAT = True
    SECOND_BEAT = False
    PULSE = False
    IBI = 600
    RATE = [0] * 10
    AMP = 100

    def __init__(self):
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.last_time = now()

    def run(self):
        # Main loop. use Ctrl-c to stop the code
        signal = self.adc.read_adc(0, gain=self.GAIN)
        current_time = now()
        self.SAMPLE_COUNTER += current_time - self.last_time
        self.last_time = current_time
        n = self.SAMPLE_COUNTER - self.LAST_BEAT_TIME
        # find the peak and trough of the pulse wave
        if signal < self.THRESH and n > (self.IBI / 5.0) * 3.0:
            # avoid dichrotic noise by waiting 3/5 of last IBI
            if signal < self.T:
                self.T = signal  # keep track of lowest point in pulse wave
        if signal > self.THRESH and signal > self.P:
            # thresh condition helps avoid noise
            self.P = signal  # keep track of highest point in pulse wave
        # signal surges up in value every time there is a pulse
        if n > 250:
            if (
                signal > self.THRESH
                and not self.PULSE
                and n > (self.IBI / 5.0) * 3.0
            ):
                # set the PULSE flag when we think there is a pulse
                self.PULSE = True
                # measure time between beats in mS
                self.IBI = self.SAMPLE_COUNTER - self.LAST_BEAT_TIME
                # keep track of time for next pulse
                self.LAST_BEAT_TIME = self.SAMPLE_COUNTER
            if self.SECOND_BEAT:
                self.SECOND_BEAT = False
                for i in range(0, 10):
                    # seed the running total to get a realisitic BPM @ start
                    self.RATE[i] = self.IBI
            if self.FIRST_BEAT:
                self.FIRST_BEAT = False
                self.SECOND_BEAT = True
                return
            # keep a running total of the last 10 IBI values
            self.RATE.pop(0)  # drop the oldest IBI value
            running_total = sum(self.RATE)  # add up the 9 oldest IBI values
            self.RATE.append(self.IBI)  # add the latest IBI to the RATE
            running_total += self.IBI  # add the latest IBI to running_total
            running_total /= 10  # average the last 10 IBI values
            BPM = 60000 / running_total
            # print('BPM: {}'.format(BPM))
            yield BPM
        # when the values are going down, the beat is over
        if signal < self.THRESH and self.PULSE:
            self.PULSE = False  # reset the PULSE flag
            self.AMP = self.P - self.T  # get amplitude of the pulse wave
            # set thresh at 50% of the amplitude
            self.THRESH = self.AMP / 2 + self.T
            # reset these for next time
            self.P = self.THRESH
            self.T = self.THRESH
        # if 2.5 seconds go by without a beat, reset
        if n > 2500:
            self.THRESH = 512
            self.P = 512
            self.T = 512
            self.LAST_BEAT_TIME = self.SAMPLE_COUNTER
            self.FIRST_BEAT = True
            self.SECOND_BEAT = False
            print("no beats found")
