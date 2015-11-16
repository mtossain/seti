#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Nov  2 14:34:22 2015
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time
import struct
import numpy as np
import os


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 3200000
        self.fftsize = fftsize = 1024

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(1420000000, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(49.6, 0)
        self.osmosdr_source_0.set_if_gain(40, 0)
        self.osmosdr_source_0.set_bb_gain(16, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=fftsize,
        	ref_scale=2,
        	frame_rate=0.5,
        	avg_alpha=0.1,
        	average=True,
        )
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, fftsize)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, "MYPIPEFFT", True)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.logpwrfft_x_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.start()
    tb.wait()
    
    
