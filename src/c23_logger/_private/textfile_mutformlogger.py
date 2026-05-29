from typing import List, TextIO
from .. import ATemporalFormattLogger

from ..exceptions import InvalidStreamTypeError



class TextfileTempFormattLogger(ATemporalFormattLogger):
	"""
		Represents an `ATemporalFormattLogger` that logs messages to a text file
	"""
	
	def __init__(
			self,
	        stream: TextIO
	):
		"""
			Creates a new TextfileTempFormattLogger
            
            Parameters
            ----------
                stream: TextIO
                    A `TextIO` object representing the output stream to be checked
                    
            Raises
            ------
                NotWritableStreamError
                    Occurs if the provided stream is not writable (and therefore it's not an output stream)
                    
                InvalidStreamTypeError
                    Occurs if the provided stream is of an invalid type with respect to the stream type
                    specified by the descendants of this abstract class
		"""
		super().__init__(stream)
		
	
	##	============================================================
	##						PRIVATE METHODS
	##	============================================================
	
	
	def _ap__assert_stream_type(self, stream: TextIO):
		parts: List[str] = stream.name.split(".")
		if len(parts) > 1:
			if parts[1] != "txt":
				raise InvalidStreamTypeError()