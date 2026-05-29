from typing import TextIO
from .. import ATemporalFormattLogger

from ..exceptions import InvalidStreamTypeError



class ConsoleTempFormattLogger(ATemporalFormattLogger):
	"""
		Represents an `ATemporalFormattLogger` that can write to the console
        (`stdout` and `stderr`)
	"""
	
	def __init__(
			self,
	        stream: TextIO,
	):
		"""
			Creates a new ConsoleTempFormattedLogger by providing the output stream
            to be associated with it
            
            Parameters
            ----------
                stream: TextIO
                    A `TextIO` object representing the output stream to be associated
			
			Raises
            ------
                NotWritableStreamError
                    Occurs if the provided stream is not writable (and therefore not an output stream)
            
                InvalidStreamTypeError
                    Occurs if the provided stream is not `stdout` or `stderr`
		"""
		super().__init__(stream)
	
	
	##	============================================================
	##						PRIVATE METHODS
	##	============================================================
	
	
	def _ap__assert_stream_type(self, stream: TextIO):
		if stream.fileno() not in [1, 2]:
			raise InvalidStreamTypeError()