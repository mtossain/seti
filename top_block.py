#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Mon Nov  9 20:36:11 2015
##################################################

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 3.2e6
        self.fc = fc = 1420e6
        self.FFTSize = FFTSize = 2**10

        ##################################################
        # Blocks
        ##################################################
        _fc_sizer = wx.BoxSizer(wx.VERTICAL)
        self._fc_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_fc_sizer,
        	value=self.fc,
        	callback=self.set_fc,
        	label='fc',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._fc_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_fc_sizer,
        	value=self.fc,
        	callback=self.set_fc,
        	minimum=1400e6,
        	maximum=1500e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_fc_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=FFTSize,
        	fft_rate=10,
        	average=False,
        	avg_alpha=0.01,
        	title="FFT Plot",
        	peak_hold=False,
        	win=window.flattop,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.osmosdr_source_1 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(fc, 0)
        self.osmosdr_source_1.set_freq_corr(0, 0)
        self.osmosdr_source_1.set_dc_offset_mode(2, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(True, 0)
        self.osmosdr_source_1.set_gain(50, 0)
        self.osmosdr_source_1.set_if_gain(20, 0)
        self.osmosdr_source_1.set_bb_gain(20, 0)
        self.osmosdr_source_1.set_antenna("", 0)
        self.osmosdr_source_1.set_bandwidth(0, 0)
          

        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_1, 0), (self.wxgui_fftsink2_0, 0))



    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self._fc_slider.set_value(self.fc)
        self._fc_text_box.set_value(self.fc)
        self.osmosdr_source_1.set_center_freq(self.fc, 0)

    def get_FFTSize(self):
        return self.FFTSize

    def set_FFTSize(self, FFTSize):
        self.FFTSize = FFTSize

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
