# audio processing class
# to take in pos audio data from queue, take the FFT of it, and get bool value of delamination
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import time


SAMPLE_RATE = 44100

class AudioProcessor():
    def __init__(self, 
                 audio_pos_queue: multiprocessing.Queue, 
                 bool_audio_pos_queue: multiprocessing.Queue,
                 fft_plot_queue: multiprocessing.Queue):
        self.audio_pos_queue = audio_pos_queue
        self.bool_audio_pos_queue = bool_audio_pos_queue
        self.fft_plot_queue = fft_plot_queue
        # define data as a numpy array
        self.data = np.array([], dtype=np.int16)

    def main(self):
        while True:
            # print("running audio processor loop")
            # if anything in queue, process audio
            if not self.audio_pos_queue.empty():
                # should be changed to process audio and not print
                self.pos, self.data = self.audio_pos_queue.get() # data is coming in as (pos, data)
                #take the FFT of the data
                fft, frequency_bins = self.perform_fft(self.data, SAMPLE_RATE)
                # check for delamination
                self.delamination = self.check_for_delamination(fft, frequency_bins)
                # get a matplotlib object of the FFT
                fft_plot = self.get_plot_object(fft, frequency_bins)
                # plt.show()
                # send the plot to main, and all the data to the plotter
                self.bool_audio_pos_queue.put((self.delamination, self.data, self.pos))
                self.fft_plot_queue.put((fft, frequency_bins))





    def perform_fft(self, signal, sample_rate):
        # perform the FFT
        fft = np.fft.fft(signal)
        # calculate the frequency bins
        frequency_bins = np.fft.fftfreq(len(signal), 1 / sample_rate)
        return fft, frequency_bins
    
    def check_for_delamination(self, fft, frequency_bins) -> bool:
        # check for delamination
        # insert algorithm here

        # for now return random boolean
        return np.random.choice([True, False])
    
    def get_plot_object(self, fft, frequency_bins):
        # get a matplotlib object of the FFT
        fig = Figure(figsize=(2,1), dpi = 800)
        ax = fig.add_subplot()
        #plot the FFT against the frequency bins
        ax.plot(frequency_bins, np.abs(fft))
        
        return fig

        

