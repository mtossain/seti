#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Sat Nov  7 17:26:12 2015
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
        self.samp_rate = samp_rate = 10e6
        self.rfgain = rfgain = 10
        self.quadrature = quadrature = 500e3
        self.ifgain = ifgain = 8
        self.freq = freq = 1420e6
        self.fftsize = fftsize = pow(2,10)
        self.cutoff = cutoff = 100e3
        self.bbgain = bbgain = 10

        ##################################################
        # Blocks
        ##################################################
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
        	average=True,
        	avg_alpha=0.00001,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        _rfgain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rfgain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rfgain_sizer,
        	value=self.rfgain,
        	callback=self.set_rfgain,
        	label='rfgain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rfgain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rfgain_sizer,
        	value=self.rfgain,
        	callback=self.set_rfgain,
        	minimum=0,
        	maximum=40,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_rfgain_sizer)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(100e6, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        _ifgain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._ifgain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_ifgain_sizer,
        	value=self.ifgain,
        	callback=self.set_ifgain,
        	label='ifgain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._ifgain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_ifgain_sizer,
        	value=self.ifgain,
        	callback=self.set_ifgain,
        	minimum=0,
        	maximum=40,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_ifgain_sizer)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=1400e6,
        	maximum=1440e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_sizer)
        _bbgain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._bbgain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_bbgain_sizer,
        	value=self.bbgain,
        	callback=self.set_bbgain,
        	label='bbgain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._bbgain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_bbgain_sizer,
        	value=self.bbgain,
        	callback=self.set_bbgain,
        	minimum=0,
        	maximum=40,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_bbgain_sizer)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0, 0), (self.wxgui_fftsink2_0, 0))



    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self._rfgain_slider.set_value(self.rfgain)
        self._rfgain_text_box.set_value(self.rfgain)

    def get_quadrature(self):
        return self.quadrature

    def set_quadrature(self, quadrature):
        self.quadrature = quadrature

    def get_ifgain(self):
        return self.ifgain

    def set_ifgain(self, ifgain):
        self.ifgain = ifgain
        self._ifgain_slider.set_value(self.ifgain)
        self._ifgain_text_box.set_value(self.ifgain)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize

    def get_cutoff(self):
        return self.cutoff

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff

    def get_bbgain(self):
        return self.bbgain

    def set_bbgain(self, bbgain):
        self.bbgain = bbgain
        self._bbgain_slider.set_value(self.bbgain)
        self._bbgain_text_box.set_value(self.bbgain)

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
