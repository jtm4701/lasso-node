#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Record Ref
# GNU Radio version: 3.8.2.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, blocks
import datetime
import osmosdr
import time
import pmt


class record_ref(gr.top_block):

    def __init__(self, center_freq=97000000, channel_freq=97900000, file_loc="/tmp/lasso_capture", hackrf_index=0, num_samples=10000000, samp_rate=2000000):
        gr.top_block.__init__(self, "Record Ref")

        ##################################################
        # Parameters
        ##################################################
        self.center_freq = center_freq
        self.channel_freq = channel_freq
        self.file_loc = file_loc
        self.hackrf_index = hackrf_index
        self.num_samples = num_samples
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'hackrf=0,bias=1'
        )
        self.osmosdr_source_0.set_clock_source('external', 0)
        self.osmosdr_source_0.set_time_source('external', 0)
        self.osmosdr_source_0.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(20, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, num_samples)
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, file_loc+"_END_"+str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace(".","_"), samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, pmt.make_dict(), False)
        self.blocks_file_meta_sink_0.set_unbuffered(False)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, center_freq - channel_freq, 1, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_meta_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_head_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0, 0))


    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.analog_sig_source_x_0.set_frequency(self.center_freq - self.channel_freq)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)

    def get_channel_freq(self):
        return self.channel_freq

    def set_channel_freq(self, channel_freq):
        self.channel_freq = channel_freq
        self.analog_sig_source_x_0.set_frequency(self.center_freq - self.channel_freq)

    def get_file_loc(self):
        return self.file_loc

    def set_file_loc(self, file_loc):
        self.file_loc = file_loc
        self.blocks_file_meta_sink_0.open(self.file_loc+"_END_"+str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace(".","_"))

    def get_hackrf_index(self):
        return self.hackrf_index

    def set_hackrf_index(self, hackrf_index):
        self.hackrf_index = hackrf_index

    def get_num_samples(self):
        return self.num_samples

    def set_num_samples(self, num_samples):
        self.num_samples = num_samples
        self.blocks_head_0.set_length(self.num_samples)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--center-freq", dest="center_freq", type=intx, default=97000000,
        help="Set center_freq [default=%(default)r]")
    parser.add_argument(
        "--channel-freq", dest="channel_freq", type=intx, default=97900000,
        help="Set channel_freq [default=%(default)r]")
    parser.add_argument(
        "--hackrf-index", dest="hackrf_index", type=intx, default=0,
        help="Set hackrf_index [default=%(default)r]")
    parser.add_argument(
        "--num-samples", dest="num_samples", type=intx, default=10000000,
        help="Set num_samples [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=intx, default=2000000,
        help="Set samp_rate [default=%(default)r]")
    return parser


def main(top_block_cls=record_ref, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(center_freq=options.center_freq, channel_freq=options.channel_freq, hackrf_index=options.hackrf_index, num_samples=options.num_samples, samp_rate=options.samp_rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
