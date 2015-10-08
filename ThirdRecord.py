#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Thirdrecord
# Generated: Thu Oct  8 17:00:30 2015
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

from PyQt4 import Qt
from datetime import datetime
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import sys
import time


class ThirdRecord(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Thirdrecord")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Thirdrecord")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ThirdRecord")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.prefix = prefix = "/home/michel/seti_"
        self.samp_rate = samp_rate = 2.4e6
        self.recfile = recfile = prefix + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log"
        self.fftsize = fftsize = pow(2,12)

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(1420e6, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(10, 0)
        self.osmosdr_source_0.set_bb_gain(10, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=fftsize,
        	ref_scale=2,
        	frame_rate=1,
        	avg_alpha=0.05,
        	average=True,
        )
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, fftsize)
        self.blocks_vector_source_x_0 = blocks.vector_source_f([0]*fftsize, True, fftsize, [])
        self.blocks_sub_xx_0 = blocks.sub_ff(fftsize)
        self.blocks_stream_to_vector_2 = blocks.stream_to_vector(gr.sizeof_char*1, fftsize)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*fftsize, recfile, False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_stream_to_vector_2, 0))    
        self.connect((self.blocks_stream_to_vector_2, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_float_to_char_0, 0))    
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.logpwrfft_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ThirdRecord")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_recfile(self.prefix + datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".log")

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_recfile(self):
        return self.recfile

    def set_recfile(self, recfile):
        self.recfile = recfile
        self.blocks_file_sink_0.open(self.recfile)

    def get_fftsize(self):
        return self.fftsize

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize
        self.blocks_vector_source_x_0.set_data([0]*self.fftsize, [])


def main(top_block_cls=ThirdRecord, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
