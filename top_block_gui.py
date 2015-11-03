#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block Gui
# Generated: Tue Oct 27 20:59:48 2015
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
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import threading
import time
import wx


class top_block_gui(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block Gui")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.prefix = prefix = "/media/michel/SETI/" + datetime.now().strftime("%Y/%Y%m%d") 
        self.samp_rate = samp_rate = 10e6
        self.record = record = 0
        self.fftsize = fftsize = pow(2,11)
        self.fftfile = fftfile = prefix+"/fft_" + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log"
        self.datafile = datafile = prefix+"/data_" + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log"

        ##################################################
        # Blocks
        ##################################################
        self.blocks_threshold_ff_0 = blocks.threshold_ff(-1000, 0, 0)
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
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(1420e6, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(15, 0)
        self.osmosdr_source_0.set_if_gain(8, 0)
        self.osmosdr_source_0.set_bb_gain(10, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=fftsize,
        	ref_scale=2,
        	frame_rate=30,
        	avg_alpha=0.01,
        	average=True,
        )
        self.fft_filter_xxx_1_0_0 = filter.fft_filter_ccc(1, ([-0.0, -3.605747770052403e-05, -0.00015325035201385617, -0.00036445073783397675, -0.0006814244552515447, -0.0011145577300339937, -0.0016726029571145773, -0.0023624503519386053, -0.0031889283563941717, -0.004154636990278959, -0.005259823519736528, -0.006502292584627867, -0.00787736289203167, -0.009377875365316868, -0.010994228534400463, -0.01271448191255331, -0.014524486847221851, -0.01640806719660759, -0.01834724098443985, -0.020322468131780624, -0.022312942892313004, -0.02429690770804882, -0.026251977309584618, -0.02815551497042179, -0.029984958469867706, -0.03171820938587189, -0.033333972096443176, -0.03481213003396988, -0.036134038120508194, -0.03728286176919937, -0.0382438525557518, -0.03900458663702011, -0.039555177092552185, -0.03988843783736229, 1.9600005149841309, -0.03988843783736229, -0.039555177092552185, -0.03900458663702011, -0.0382438525557518, -0.03728286176919937, -0.036134038120508194, -0.03481213003396988, -0.033333972096443176, -0.03171820938587189, -0.029984958469867706, -0.02815551497042179, -0.026251977309584618, -0.02429690770804882, -0.022312942892313004, -0.020322468131780624, -0.01834724098443985, -0.01640806719660759, -0.014524486847221851, -0.01271448191255331, -0.010994228534400463, -0.009377875365316868, -0.00787736289203167, -0.006502292584627867, -0.005259823519736528, -0.004154636990278959, -0.0031889283563941717, -0.0023624503519386053, -0.0016726029571145773, -0.0011145577300339937, -0.0006814244552515447, -0.00036445073783397675, -0.00015325035201385617, -3.605747770052403e-05, -0.0]), 1)
        self.fft_filter_xxx_1_0_0.declare_sample_delay(0)
        self.fft_filter_xxx_1_0 = filter.fft_filter_ccc(1, ([-9.537214351595935e-10, -0.000768458703532815, 0.0035646669566631317, -0.009442212991416454, 0.019308455288410187, -0.03309587016701698, 0.049214430153369904, -0.06466702371835709, 0.07588998228311539, 1.9199920892715454, 0.07588998228311539, -0.06466703116893768, 0.049214426428079605, -0.03309587016701698, 0.019308457151055336, -0.009442214854061604, 0.0035646690521389246, -0.0007684589363634586, -9.537214351595935e-10]), 1)
        self.fft_filter_xxx_1_0.declare_sample_delay(0)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, fftsize)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, fftsize)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_char, fftsize, 100*fftsize, 0)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, 10000*fftsize)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*fftsize, fftfile, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, datafile, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blks2_valve_0 = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(1-record))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_valve_0, 0), (self.blocks_head_0, 0))    
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_keep_m_in_n_0, 0))    
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_char_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.fft_filter_xxx_1_0, 0), (self.fft_filter_xxx_1_0_0, 0))    
        self.connect((self.fft_filter_xxx_1_0_0, 0), (self.blks2_valve_0, 0))    
        self.connect((self.fft_filter_xxx_1_0_0, 0), (self.logpwrfft_x_0, 0))    
        self.connect((self.fft_filter_xxx_1_0_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.fft_filter_xxx_1_0, 0))    


    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_datafile(self.prefix+"/data_" + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log")
        self.set_fftfile(self.prefix+"/fft_" + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log")

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

    def get_record(self):
        return self.record

    def set_record(self, record):
        self.record = record
        self.blks2_valve_0.set_open(bool(1-self.record))

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
    tb = top_block_gui()
    tb.Start(True)
    tb.Wait()