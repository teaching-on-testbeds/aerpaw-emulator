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


class LW_CS(gr.top_block):
    def __init__(self, args="", freq=3.32e9, gainrx=30, gaintx=76, rxfreq=187.5e3, txfreq1=812.5e3, txfreq2=-312.5e3):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Parameters
        ##################################################
        self.args = args
        self.freq = freq
        self.gainrx = gainrx
        self.gaintx = gaintx
        self.rxfreq = rxfreq
        self.txfreq1 = txfreq1
        self.txfreq2 = txfreq2

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
                channels=list(range(0, 2)),
            ),
        )
        self.uhd_usrp_source_1.set_time_source("external", 0)
        self.uhd_usrp_source_1.set_clock_source("external", 0)
        self.uhd_usrp_source_1.set_center_freq(freq, 0)
        self.uhd_usrp_source_1.set_gain(gainrx, 0)
        self.uhd_usrp_source_1.set_antenna("RX2", 0)
        self.uhd_usrp_source_1.set_center_freq(freq, 1)
        self.uhd_usrp_source_1.set_gain(gainrx, 1)
        self.uhd_usrp_source_1.set_antenna("RX2", 1)
        self.uhd_usrp_source_1.set_samp_rate(samp_rate)
        self.uhd_usrp_source_1.set_time_unknown_pps(uhd.time_spec())
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", args)),
            uhd.stream_args(
                cpu_format="fc32",
                args="",
                channels=list(range(0, 2)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_time_source("external", 0)
        self.uhd_usrp_sink_0.set_clock_source("external", 0)
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(gaintx, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_center_freq(freq, 1)
        self.uhd_usrp_sink_0.set_gain(gaintx, 1)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 1)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec())
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(1 / 1.58)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1 / 1.58)
        self.blocks_file_sink_0_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality2", False)
        self.blocks_file_sink_0_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Quality1", False)
        self.blocks_file_sink_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power2", False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float * 1, "/root/Power1", False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.SounderTX_0_0 = SounderTX(
            alpha=alpha,
            freq=txfreq2,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderTX_0 = SounderTX(
            alpha=alpha,
            freq=txfreq1,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq,
            ftrans=20e3,
            gainrx=gainrx,
            samp_rate=samp_rate,
            sps=sps,
        )
        self.SounderRX_0 = SounderRX(
            fcut=62.5e3,
            freq=rxfreq,
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
        self.connect((self.SounderTX_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.SounderTX_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.uhd_usrp_sink_0, 1))
        self.connect((self.uhd_usrp_source_1, 0), (self.SounderRX_0, 0))
        self.connect((self.uhd_usrp_source_1, 1), (self.SounderRX_0_0, 0))

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
        self.uhd_usrp_source_1.set_gain(self.gainrx, 0)
        self.uhd_usrp_source_1.set_gain(self.gainrx, 1)

    def get_gaintx(self):
        return self.gaintx

    def set_gaintx(self, gaintx):
        self.gaintx = gaintx
        self.uhd_usrp_sink_0.set_gain(self.gaintx, 0)
        self.uhd_usrp_sink_0.set_gain(self.gaintx, 1)

    def get_rxfreq(self):
        return self.rxfreq

    def set_rxfreq(self, rxfreq):
        self.rxfreq = rxfreq
        self.SounderRX_0.set_freq(self.rxfreq)
        self.SounderRX_0_0.set_freq(self.rxfreq)

    def get_txfreq1(self):
        return self.txfreq1

    def set_txfreq1(self, txfreq1):
        self.txfreq1 = txfreq1
        self.SounderTX_0.set_freq(self.txfreq1)

    def get_txfreq2(self):
        return self.txfreq2

    def set_txfreq2(self, txfreq2):
        self.txfreq2 = txfreq2
        self.SounderTX_0_0.set_freq(self.txfreq2)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.SounderRX_0.set_sps(self.sps)
        self.SounderRX_0_0.set_sps(self.sps)
        self.SounderTX_0.set_sps(self.sps)
        self.SounderTX_0_0.set_sps(self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.SounderRX_0.set_samp_rate(self.samp_rate)
        self.SounderRX_0_0.set_samp_rate(self.samp_rate)
        self.SounderTX_0.set_samp_rate(self.samp_rate)
        self.SounderTX_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_1.set_samp_rate(self.samp_rate)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.SounderTX_0.set_alpha(self.alpha)
        self.SounderTX_0_0.set_alpha(self.alpha)


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument("--args", dest="args", type=str, default="", help="Set args [default=%(default)r]")
    parser.add_argument("--freq", dest="freq", type=eng_float, default="3.32G", help="Set freq [default=%(default)r]")
    parser.add_argument("--gainrx", dest="gainrx", type=eng_float, default="30.0", help="Set gainrx [default=%(default)r]")
    parser.add_argument("--gaintx", dest="gaintx", type=eng_float, default="76.0", help="Set gaintx [default=%(default)r]")
    parser.add_argument("--rxfreq", dest="rxfreq", type=eng_float, default="187.5k", help="Set rxfreq [default=%(default)r]")
    parser.add_argument("--txfreq1", dest="txfreq1", type=eng_float, default="812.5k", help="Set txfreq1 [default=%(default)r]")
    parser.add_argument("--txfreq2", dest="txfreq2", type=eng_float, default="-312.5k", help="Set txfreq2 [default=%(default)r]")
    return parser


def main(top_block_cls=LW_CS, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(args=options.args, freq=options.freq, gainrx=options.gainrx, gaintx=options.gaintx, rxfreq=options.rxfreq, txfreq1=options.txfreq1, txfreq2=options.txfreq2)

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
