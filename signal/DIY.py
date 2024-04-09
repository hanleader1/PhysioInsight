from PhysioInsight.signal.Signal import Signal


class DIY(Signal):
    def __init__(self, local_signal, duration, sampling_rate):
        super().__init__(duration, sampling_rate, local_signal)
        self.signal_name = type(self).__name__

    def copy(self):
        return DIY(self.signal, self.duration, self.sampling_rate)