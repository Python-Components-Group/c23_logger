"""
Python autonomous component which provides logging services for any Python software system
"""

from . import exceptions

from ._private.i_formattable_logger import IFormattableLogger
from ._private.a_temporal_formlogger import ATemporalFormattLogger

from ._private.textfile_mutformlogger import TextfileTempFormattLogger
from ._private.console_formlogger import ConsoleTempFormattLogger