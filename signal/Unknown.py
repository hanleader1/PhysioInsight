import neurokit2 as nk
from PhysioInsight.signal.Signal import Signal


class Unknown(Signal):
    def __init__(self, duration, sampling_rate, noise, frequency, amplitude):
        super().__init__(duration, sampling_rate)
        self.signal_name = type(self).__name__
        self.noise = noise
        self.frequency = frequency
        self.amplitude = amplitude
        self.signal=self.generate_signal()

    def generate_signal(self):
        # 生成 ECG 信号的方法
        return nk.signal_simulate(duration=self.duration, noise=self.noise,sampling_rate=self.sampling_rate,
                                  amplitude=self.amplitude, frequency=self.frequency)

