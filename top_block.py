#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sun Oct 18 22:54:11 2015
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

from datetime import datetime
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
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
        self.prefixfft = prefixfft = "/media/michel/SETI/fft_"
        self.prefixdata = prefixdata = "/media/michel/SETI/data_"
        self.samp_rate = samp_rate = 10e6
        self.record = record = 0
        self.intamp = intamp = 20e-6
        self.fftsize = fftsize = pow(2,11)
        self.fftfile = fftfile = prefixfft + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log"
        self.datafile = datafile = prefixdata + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log"

        ##################################################
        # Blocks
        ##################################################
        self.blocks_threshold_ff_0 = blocks.threshold_ff(-1000, -78, 0)
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
        self.fft_filter_xxx_1 = filter.fft_filter_ccc(1, ([0.07469794899225235, 1.8506040573120117, 0.07469794899225235]), 1)
        self.fft_filter_xxx_1.declare_sample_delay(0)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, ([-0.0010990326991304755, -0.0011334356386214495, -0.0011985328746959567, -0.001295603928156197, -0.0014257250586524606, -0.0015897577395662665, -0.0017883378313854337, -0.002021867549046874, -0.002290506847202778, -0.0025941694620996714, -0.0029325177893042564, -0.003304962767288089, -0.0037106613162904978, -0.004148522391915321, -0.0046172053553164005, -0.005115131381899118, -0.005640486720949411, -0.006191234104335308, -0.006765123922377825, -0.007359706796705723, -0.007972347550094128, -0.00860024243593216, -0.00924043171107769, -0.009889830835163593, -0.010545231401920319, -0.011203338392078876, -0.011860785074532032, -0.012514152564108372, -0.01316000148653984, -0.013794880360364914, -0.01441536657512188, -0.015018078498542309, -0.015599698759615421, -0.016157003119587898, -0.016686875373125076, -0.01718633621931076, -0.017652561888098717, -0.01808289811015129, -0.0184748824685812, -0.01882627233862877, -0.019135037437081337, -0.01939939707517624, -0.019617818295955658, -0.019789034500718117, -0.019912049174308777, -0.019986147060990334, 1.9810783863067627, -0.019986147060990334, -0.019912049174308777, -0.019789034500718117, -0.019617818295955658, -0.01939939707517624, -0.019135037437081337, -0.01882627233862877, -0.0184748824685812, -0.01808289811015129, -0.017652561888098717, -0.01718633621931076, -0.016686875373125076, -0.016157003119587898, -0.015599698759615421, -0.015018078498542309, -0.01441536657512188, -0.013794880360364914, -0.01316000148653984, -0.012514152564108372, -0.011860785074532032, -0.011203338392078876, -0.010545231401920319, -0.009889830835163593, -0.00924043171107769, -0.00860024243593216, -0.007972347550094128, -0.007359706796705723, -0.006765123922377825, -0.006191234104335308, -0.005640486720949411, -0.005115131381899118, -0.0046172053553164005, -0.004148522391915321, -0.0037106613162904978, -0.003304962767288089, -0.0029325177893042564, -0.0025941694620996714, -0.002290506847202778, -0.002021867549046874, -0.0017883378313854337, -0.0015897577395662665, -0.0014257250586524606, -0.001295603928156197, -0.0011985328746959567, -0.0011334356386214495, -0.0010990326991304755]), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, fftsize)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, fftsize)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_char, fftsize, 100*fftsize, 0)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, 10000*fftsize)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*fftsize, fftfile, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, datafile, False)
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
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_keep_m_in_n_0, 0))    
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_char_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.fft_filter_xxx_1, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.fft_filter_xxx_1, 0))    


    def get_prefixfft(self):
        return self.prefixfft

    def set_prefixfft(self, prefixfft):
        self.prefixfft = prefixfft
        self.set_fftfile(self.prefixfft + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log")

    def get_prefixdata(self):
        return self.prefixdata

    def set_prefixdata(self, prefixdata):
        self.prefixdata = prefixdata
        self.set_datafile(self.prefixdata + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log")

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
        self.blocks_head_0.set_length(10000*self.fftsize)
        self.blocks_keep_m_in_n_0.set_m(self.fftsize)
        self.blocks_keep_m_in_n_0.set_n(100*self.fftsize)

    def get_fftfile(self):
        return self.fftfile

    def set_fftfile(self, fftfile):
        self.fftfile = fftfile
        self.blocks_file_sink_0_0.open(self.fftfile)

    def get_datafile(self):
        return self.datafile

    def set_datafile(self, datafile):
        self.datafile = datafile
        self.blocks_file_sink_0.open(self.datafile)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
