#!/usr/bin/env python3

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: v3.8.5.0-6-g57bd109d

import os
import sys

sys.path.append(os.environ.get("GRC_HIER_PATH", os.path.expanduser("~/.grc_gnuradio")))

import signal
from argparse import ArgumentParser

from gnuradio import blocks, gr, uhd
from gnuradio.eng_arg import eng_float
from SounderRX import SounderRX  # grc-generated hier_block
from SounderTX import SounderTX  # grc-generated hier_block


class LPN_CS(gr.top_block):
    def __init__(self, args="", freq=3.32e9, gainrx=30, gaintx=76, rxfreq1=812.5e3, rxfreq10=-812.5e3, rxfreq2=-312.5e3, rxfreq3=687.5e3, rxfreq4=-437.5e3, rxfreq5=562.5e3, rxfreq6=-562.5e3, rxfreq7=437.5e3, rxfreq8=-687.5e3, rxfreq9=312.5e3, txfreq=187.5e3):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Parameters
        ##################################################
        self.args = args
        self.freq = freq
        self.gainrx = gainrx
        self.gaintx = gaintx
        self.rxfreq1 = rxfreq1
        self.rxfreq10 = rxfreq10
        self.rxfreq2 = rxfreq2
        self.rxfreq3 = rxfreq3
        self.rxfreq4 = rxfreq4
        self.rxfreq5 = rxfreq5
        self.rxfreq6 = rxfreq6
        self.rxfreq7 = rxfreq7
        self.rxfreq8 = rxfreq8
        self.rxfreq9 = rxfreq9
        self.txfreq = txfreq

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 32
        self.samp_rate = samp_rate = 2e6
        self.alpha = alpha = 0.99

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_1 = uhd.usrp_source(
            ",".join(("", args)),
            uhd.stream_args(
                cpu_format="fc32",
                args="",
                channels=list(range(0, 1)),
            ),
        )
        self.uhd_usrp_source_1.set_time_source("external", 0)
        self.uhd_usrp_source_1.set_clock_source("external", 0)
        self.uhd_usrp_source_1.set_center_freq(freq, 0)
        self.uhd_usrp_source_1.set_gain(gainrx, 0)
        self.uhd_usrp_source_1.set_antenna("RX2", 0)
        self.uhd_usrp_source_1.set_samp_rate(samp_rate)
        self.uhd_usrp_source_1.set_time_unknown_pps(uhd.time_spec())
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", args)),
            uhd.stream_args(
                cpu_format="fc32",
                args="",
                channels=list(range(0, 1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_time_source("external", 0)
        self.uhd_usrp_sink_0.set_clock_source("external", 0)
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(gaintx, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec())
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1 / 1.58)
        self.blocks_file_sink_0_0_1_0_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power10", False)
        self.blocks_file_sink_0_0_1_0_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_1_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power9", False)
        self.blocks_file_sink_0_0_1_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_1_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power8", False)
        self.blocks_file_sink_0_0_1_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_1_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power7", False)
        self.blocks_file_sink_0_0_1_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_1_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power6", False)
        self.blocks_file_sink_0_0_1_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_1_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power5", False)
        self.blocks_file_sink_0_0_1_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_1_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power4", False)
        self.blocks_file_sink_0_0_1_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_1 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power3", False)
        self.blocks_file_sink_0_0_1.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_0_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality10", False)
        self.blocks_file_sink_0_0_0_0_0_0_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality9", False)
        self.blocks_file_sink_0_0_0_0_0_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality8", False)
        self.blocks_file_sink_0_0_0_0_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality7", False)
        self.blocks_file_sink_0_0_0_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality6", False)
        self.blocks_file_sink_0_0_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality5", False)
        self.blocks_file_sink_0_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality4", False)
        self.blocks_file_sink_0_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality3", False)
        self.blocks_file_sink_0_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality2", False)
        self.blocks_file_sink_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality1", False)
        self.blocks_file_sink_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power2", False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power1", False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.SounderTX_0 = SounderTX(
            alpha=alpha,
            freq=txfreq,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0_0_0_0_0_0_0_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq10,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0_0_0_0_0_0_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq9,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0_0_0_0_0_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq8,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0_0_0_0_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq7,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0_0_0_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq6,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0_0_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq5,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq4,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq3,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq2,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq1,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.SounderRX_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.SounderRX_0, 1), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.SounderRX_0_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.SounderRX_0_0, 1), (self.blocks_file_sink_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0, 1), (self.blocks_file_sink_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0, 0), (self.blocks_file_sink_0_0_1, 0))
        self.connect((self.SounderRX_0_0_0_0, 1), (self.blocks_file_sink_0_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0, 0), (self.blocks_file_sink_0_0_1_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0, 1), (self.blocks_file_sink_0_0_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0, 0), (self.blocks_file_sink_0_0_1_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0, 1), (self.blocks_file_sink_0_0_0_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0, 0), (self.blocks_file_sink_0_0_1_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0_0, 1), (self.blocks_file_sink_0_0_0_0_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0_0, 0), (self.blocks_file_sink_0_0_1_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0_0_0, 1), (self.blocks_file_sink_0_0_0_0_0_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0_0_0, 0), (self.blocks_file_sink_0_0_1_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0_0_0_0, 1), (self.blocks_file_sink_0_0_0_0_0_0_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0_0_0_0, 0), (self.blocks_file_sink_0_0_1_0_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0_0_0_0_0, 1), (self.blocks_file_sink_0_0_0_0_0_0_0_0_0_0_0_0, 0))
        self.connect((self.SounderRX_0_0_0_0_0_0_0_0_0_0, 0), (self.blocks_file_sink_0_0_1_0_0_0_0_0_0_0, 0))
        self.connect((self.SounderTX_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0_0_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0_0_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0_0_0_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0_0_0_0_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0_0_0_0_0_0_0_0_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0_0_0_0_0_0_0_0_0_0, 0))

    def get_args(self):
        return self.args

    def set_args(self, args):
        self.args = args

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 1)
        self.uhd_usrp_source_1.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_1.set_center_freq(self.freq, 1)

    def get_gainrx(self):
        return self.gainrx

    def set_gainrx(self, gainrx):
        self.gainrx = gainrx
        self.SounderRX_0.set_gainrx(self.gainrx)
        self.SounderRX_0_0.set_gainrx(self.gainrx)
        self.SounderRX_0_0_0.set_gainrx(self.gainrx)
        self.SounderRX_0_0_0_0.set_gainrx(self.gainrx)
        self.SounderRX_0_0_0_0_0.set_gainrx(self.gainrx)
        self.SounderRX_0_0_0_0_0_0.set_gainrx(self.gainrx)
        self.SounderRX_0_0_0_0_0_0_0.set_gainrx(self.gainrx)
        self.SounderRX_0_0_0_0_0_0_0_0.set_gainrx(self.gainrx)
        self.SounderRX_0_0_0_0_0_0_0_0_0.set_gainrx(self.gainrx)
        self.SounderRX_0_0_0_0_0_0_0_0_0_0.set_gainrx(self.gainrx)
        self.uhd_usrp_source_1.set_gain(self.gainrx, 0)
        self.uhd_usrp_source_1.set_gain(self.gainrx, 1)

    def get_gaintx(self):
        return self.gaintx

    def set_gaintx(self, gaintx):
        self.gaintx = gaintx
        self.uhd_usrp_sink_0.set_gain(self.gaintx, 0)
        self.uhd_usrp_sink_0.set_gain(self.gaintx, 1)

    def get_rxfreq1(self):
        return self.rxfreq1

    def set_rxfreq1(self, rxfreq1):
        self.rxfreq1 = rxfreq1
        self.SounderRX_0.set_freq(self.rxfreq1)

    def get_rxfreq10(self):
        return self.rxfreq10

    def set_rxfreq10(self, rxfreq10):
        self.rxfreq10 = rxfreq10
        self.SounderRX_0_0_0_0_0_0_0_0_0_0.set_freq(self.rxfreq10)

    def get_rxfreq2(self):
        return self.rxfreq2

    def set_rxfreq2(self, rxfreq2):
        self.rxfreq2 = rxfreq2
        self.SounderRX_0_0.set_freq(self.rxfreq2)

    def get_rxfreq3(self):
        return self.rxfreq3

    def set_rxfreq3(self, rxfreq3):
        self.rxfreq3 = rxfreq3
        self.SounderRX_0_0_0.set_freq(self.rxfreq3)

    def get_rxfreq4(self):
        return self.rxfreq4

    def set_rxfreq4(self, rxfreq4):
        self.rxfreq4 = rxfreq4
        self.SounderRX_0_0_0_0.set_freq(self.rxfreq4)

    def get_rxfreq5(self):
        return self.rxfreq5

    def set_rxfreq5(self, rxfreq5):
        self.rxfreq5 = rxfreq5
        self.SounderRX_0_0_0_0_0.set_freq(self.rxfreq5)

    def get_rxfreq6(self):
        return self.rxfreq6

    def set_rxfreq6(self, rxfreq6):
        self.rxfreq6 = rxfreq6
        self.SounderRX_0_0_0_0_0_0.set_freq(self.rxfreq6)

    def get_rxfreq7(self):
        return self.rxfreq7

    def set_rxfreq7(self, rxfreq7):
        self.rxfreq7 = rxfreq7
        self.SounderRX_0_0_0_0_0_0_0.set_freq(self.rxfreq7)

    def get_rxfreq8(self):
        return self.rxfreq8

    def set_rxfreq8(self, rxfreq8):
        self.rxfreq8 = rxfreq8
        self.SounderRX_0_0_0_0_0_0_0_0.set_freq(self.rxfreq8)

    def get_rxfreq9(self):
        return self.rxfreq9

    def set_rxfreq9(self, rxfreq9):
        self.rxfreq9 = rxfreq9
        self.SounderRX_0_0_0_0_0_0_0_0_0.set_freq(self.rxfreq9)

    def get_txfreq(self):
        return self.txfreq

    def set_txfreq(self, txfreq):
        self.txfreq = txfreq
        self.SounderTX_0.set_freq(self.txfreq)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.SounderRX_0.set_sps(self.sps)
        self.SounderRX_0_0.set_sps(self.sps)
        self.SounderRX_0_0_0.set_sps(self.sps)
        self.SounderRX_0_0_0_0.set_sps(self.sps)
        self.SounderRX_0_0_0_0_0.set_sps(self.sps)
        self.SounderRX_0_0_0_0_0_0.set_sps(self.sps)
        self.SounderRX_0_0_0_0_0_0_0.set_sps(self.sps)
        self.SounderRX_0_0_0_0_0_0_0_0.set_sps(self.sps)
        self.SounderRX_0_0_0_0_0_0_0_0_0.set_sps(self.sps)
        self.SounderRX_0_0_0_0_0_0_0_0_0_0.set_sps(self.sps)
        self.SounderTX_0.set_sps(self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.SounderRX_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0_0_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0_0_0_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0_0_0_0_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0_0_0_0_0_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0_0_0_0_0_0_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0_0_0_0_0_0_0_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0_0_0_0_0_0_0_0_0.set_samp_rate(self.samp_rate)
        self.SounderTX_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_1.set_samp_rate(self.samp_rate)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.SounderTX_0.set_alpha(self.alpha)


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument("--args", dest="args", type=str, default="", help="Set args [default=%(default)r]")
    parser.add_argument("--freq", dest="freq", type=eng_float, default="3.32G", help="Set freq [default=%(default)r]")
    parser.add_argument("--gainrx", dest="gainrx", type=eng_float, default="30.0", help="Set gainrx [default=%(default)r]")
    parser.add_argument("--gaintx", dest="gaintx", type=eng_float, default="76.0", help="Set gaintx [default=%(default)r]")
    parser.add_argument("--rxfreq1", dest="rxfreq1", type=eng_float, default="812.5k", help="Set rxfreq1 [default=%(default)r]")
    parser.add_argument("--rxfreq10", dest="rxfreq10", type=eng_float, default="-812.5k", help="Set rxfreq10 [default=%(default)r]")
    parser.add_argument("--rxfreq2", dest="rxfreq2", type=eng_float, default="-312.5k", help="Set rxfreq2 [default=%(default)r]")
    parser.add_argument("--rxfreq3", dest="rxfreq3", type=eng_float, default="687.5k", help="Set rxfreq3 [default=%(default)r]")
    parser.add_argument("--rxfreq4", dest="rxfreq4", type=eng_float, default="-437.5k", help="Set rxfreq4 [default=%(default)r]")
    parser.add_argument("--rxfreq5", dest="rxfreq5", type=eng_float, default="562.5k", help="Set rxfreq5 [default=%(default)r]")
    parser.add_argument("--rxfreq6", dest="rxfreq6", type=eng_float, default="-562.5k", help="Set rxfreq6 [default=%(default)r]")
    parser.add_argument("--rxfreq7", dest="rxfreq7", type=eng_float, default="437.5k", help="Set rxfreq7 [default=%(default)r]")
    parser.add_argument("--rxfreq8", dest="rxfreq8", type=eng_float, default="-687.5k", help="Set rxfreq8 [default=%(default)r]")
    parser.add_argument("--rxfreq9", dest="rxfreq9", type=eng_float, default="312.5k", help="Set rxfreq9 [default=%(default)r]")
    parser.add_argument("--txfreq", dest="txfreq", type=eng_float, default="187.5k", help="Set txfreq [default=%(default)r]")
    return parser


def main(top_block_cls=LPN_CS, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(args=options.args, freq=options.freq, gainrx=options.gainrx, gaintx=options.gaintx, rxfreq1=options.rxfreq1, rxfreq10=options.rxfreq10, rxfreq2=options.rxfreq2, rxfreq3=options.rxfreq3, rxfreq4=options.rxfreq4, rxfreq5=options.rxfreq5, rxfreq6=options.rxfreq6, rxfreq7=options.rxfreq7, rxfreq8=options.rxfreq8, rxfreq9=options.rxfreq9, txfreq=options.txfreq)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input("Press Enter to quit: ")
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == "__main__":
    main()
