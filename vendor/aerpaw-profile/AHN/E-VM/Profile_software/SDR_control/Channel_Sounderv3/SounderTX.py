#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SounderTX
# GNU Radio version: v3.8.5.0-6-g57bd109d


from gnuradio import analog, blocks, digital, filter, gr
from gnuradio.filter import firdes


class SounderTX(gr.hier_block2):
    def __init__(self, alpha=0.99, freq=0, samp_rate=2e6, sps=16):
        gr.hier_block2.__init__(
            self,
            "SounderTX",
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_gr_complex * 1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.alpha = alpha
        self.freq = freq
        self.samp_rate = samp_rate
        self.sps = sps

        ##################################################
        # Blocks
        ##################################################
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(sps, samp_rate, samp_rate / sps, alpha, 10 * sps + 1))
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(sps, [1] + [0] * (sps - 1))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_glfsr_source_x_0 = digital.glfsr_source_b(12, True, 0, 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((-1, 1), 1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq, 1, 0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_multiply_xx_0, 0))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.samp_rate / self.sps, self.alpha, 10 * self.sps + 1))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.analog_sig_source_x_0.set_frequency(self.freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.samp_rate / self.sps, self.alpha, 10 * self.sps + 1))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.interp_fir_filter_xxx_0.set_taps([1] + [0] * (self.sps - 1))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(self.sps, self.samp_rate, self.samp_rate / self.sps, self.alpha, 10 * self.sps + 1))
