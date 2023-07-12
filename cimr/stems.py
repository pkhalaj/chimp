"""
cimr.stems
==========

Defines factory functions for different stem types.
"""
from torch import nn

from cimr.config import InputConfig

def basic_conv(
        n_chans_in,
        n_chans_out,
        kernel_size=3,
        padding=1,
        stride=1,
):
    """
    A basic stem consisting of a single convolution layer
    of variable kernel size.
    """
    return nn.Conv2d(
        n_chans_in,
        n_chans_out,
        kernel_size,
        stride=stride,
        padding=padding
    )


def get_stem_factory(input_config: InputConfig):
    """
    Product a stem factory function that can be used to product
    stems for an encoder module.

    Args:
        input_config: An InputConfig object specifying the properties
            of the input data that this stem will be applied to.

    Return:
        A stem factory that can be used with a
        quantnn.model.pytorch.encoders.MultiInputEncoder.

    """

    n_chans_in = input_config.input_data.n_channels
    kernel_size = input_config.stem_kernel_size
    stride = input_config.stem_downsampling
    padding = kernel_size // 2

    if input_config.stem_type == "basic":
        def factory(n_chans_out):
            return basic_conv(
                n_chans_in,
                n_chans_out,
                kernel_size=kernel_size,
                stride=stride,
                padding=padding
            )
        return factory

    raise ValueError(
        "Stem type '%s' is not known.",
        input_config.stem_type
    )