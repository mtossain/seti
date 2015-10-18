#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sun Oct 18 19:45:27 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import threading
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6
        self.record = record = 1
        self.intamp = intamp = 20e-6
        self.fftsize = fftsize = pow(2,11)

        ##################################################
        # Blocks
        ##################################################
        self.blocks_threshold_ff_0 = blocks.threshold_ff(-1000, -80, 0)
        def _record_probe():
            while True:
                val = self.blocks_threshold_ff_0.last_state()
                try:
                    self.set_record(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _record_thread = threading.Thread(target=_record_probe)
        _record_thread.daemon = True
        _record_thread.start()
        _intamp_sizer = wx.BoxSizer(wx.VERTICAL)
        self._intamp_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_intamp_sizer,
        	value=self.intamp,
        	callback=self.set_intamp,
        	label='intamp',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._intamp_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_intamp_sizer,
        	value=self.intamp,
        	callback=self.set_intamp,
        	minimum=0,
        	maximum=0.001,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_intamp_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=10,
        	average=True,
        	avg_alpha=0.01,
        	title="FFT Plot",
        	peak_hold=False,
        	win=window.blackmanharris,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(1420e6, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(10, 0)
        self.osmosdr_source_0.set_bb_gain(10, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(15e6, 0)
          
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=fftsize,
        	ref_scale=2,
        	frame_rate=30,
        	avg_alpha=0.01,
        	average=True,
        )
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, fftsize)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, 1024)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/michel/test.dat", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blks2_valve_0 = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(1-record))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1421e6, intamp, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blks2_valve_0, 0), (self.blocks_head_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.blks2_valve_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.logpwrfft_x_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_null_sink_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.blocks_add_xx_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

    def get_record(self):
        return self.record

    def set_record(self, record):
        self.record = record
        self.blks2_valve_0.set_open(bool(1-self.record))

    def get_intamp(self):
        return self.intamp

    def set_intamp(self, intamp):
        self.intamp = intamp
        self._intamp_slider.set_value(self.intamp)
        self._intamp_text_box.set_value(self.intamp)
        self.analog_sig_source_x_0.set_amplitude(self.intamp)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
