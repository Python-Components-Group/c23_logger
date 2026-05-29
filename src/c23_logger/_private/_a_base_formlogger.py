from typing import Set, Dict, TextIO
from abc import abstractmethod
from .. import IFormattableLogger

from string import Formatter as StrFormatter

from ..exceptions import (
	NotWritableStreamError,
	FormatNotSetError
)



class _ABaseFormattableLogger(IFormattableLogger):
	"""
		Represents a base `IFormattableLogger`, containing the control logic common to all
		`IFormattableLogger` instances.
        
        The type of output stream is specified by the descendants of this abstract class.
        Other format placeholders are specified by the descendants of this abstract class.
	"""

	def __init__(
			self,
			stream: TextIO
	):
		"""
			Creates a new _ABaseFormattableLogger by providing the output stream
            to be verified before associating it with this logger
            
            Parameters
            ----------
                    A `TextIO` object representing the output stream to be associated
                    with this logger

			Raises
			------
                NotWritableStreamError
                    Occurs if the provided stream:
					
						- The provided stream is not an output stream
                        - The provided stream is closed
            
                InvalidStreamTypeError
                    Occurs if the provided stream is of an invalid type with respect to the stream type
                    specified by the descendants of this abstract class
		"""
		if (not stream.writable()) or stream.closed:
			raise NotWritableStreamError()
		
		self._ap__assert_stream_type(stream)
		
		self._stream: TextIO = stream
		
		self._format: str = None
		self._parser: StrFormatter = StrFormatter()
		
		self._sep: str = "\n"
		self._first_message: bool = True
		
		
	def change_stream(
			self,
			new_stream: TextIO
	):
		"""
			Changes the output stream to which logger messages are written
            
            Parameters
            ----------
				new_stream: TextIO
                    A `TextIO` object representing the new output stream to use
                    
            Raises
            ------
				NotWritableStreamError
                    Occurs if the provided stream is not writable (and therefore it's not an output stream)
            
                InvalidStreamTypeError
                    Occurs if the provided stream is of an invalid type relative to the stream type
                    specified by the descendants of this abstract class
		"""
		if not new_stream.writable():
			raise NotWritableStreamError()
		
		self._ap__assert_stream_type(new_stream)
		
		self._stream = new_stream


	def set_format(
			self,
			format_str: str
	):
		if (format_str is None):
			raise ValueError()
		
		placehs: Set[str] = {
		    placeh
		    for _, placeh, _, _ in self._parser.parse(format_str)
		    if placeh is not None
		}
		placehs = placehs.difference({"message"})
		self._ap__assert_format(placehs)
		
		self._format = format_str
	
	
	def unset_format(self) -> str:
		if self._format is None:
			raise FormatNotSetError()
		
		old_format: str = self._format
		self._format = None
		return old_format
	
	
	def set_messages_sep(self, new_sep: str):
		if (new_sep is None):
			raise ValueError()
		
		self._sep = new_sep
	
	
	def log(
			self,
			message: str,
			format_: bool=True
	):
		if message is None:
			raise ValueError()
		
		log_message: str = message
		if format_:
			format_vars: Dict[str, str] = self._ap__format_vars()
			format_vars["message"] = message
			log_message = str.format_map(self._format, format_vars)
			
		if not self._first_message:
			self._stream.write(self._sep)
		else:
			self._first_message = False
		self._stream.write(log_message)
		self._stream.flush()
		
		
	##	============================================================
	##						ABSTRACT METHODS
	##	============================================================
	
	
	@abstractmethod
	def _ap__assert_stream_type(
			self,
			stream: TextIO
	):
		"""
			Checks whether the provided output stream conforms to the output stream type
			specified by the descendants of this abstract class.

			If the check succeeds, this operation is equivalent to a no-op.

			Parameters
			----------
                stream: TextIO
					A `TextIO` object representing the output stream to be verified
            
            Raises
            ------
                InvalidStreamTypeError
                    Occurs if the provided stream is of an invalid type with respect to the
                    stream type specified by the descendants of this abstract class
		"""
		pass
	
	
	@abstractmethod
	def _ap__format_vars(self) -> Dict[str, str]:
		"""
			Returns the formatting placeholders specified by the descendants of this
            abstract class and their associated values
            
            Returns
            -------
				Dict[str, str]
                    A string dictionary, indexed by strings, containing:
                    
                        - As keys: The format placeholders specified by the descendants
                        - As values: The values of those placeholders
		"""
		pass
	
	
	@abstractmethod
	def _ap__assert_format(self, placehs: Set[str]):
		"""
			Verifies that the placeholders of a given format are consistent with
			those specified by the descendants of this abstract class.
            
            If the verification succeeds, this operation is equivalent to a no-op.
            
            Parameters
            ----------
				placehs: Set[str]
                    A set of strings containing the placeholders of a new format
                    to be set
					
			Raises:
            ------
                InvalidFormatError
                    Occurs if a format was provided with placeholders different
                    from those accepted by the descendants of this abstract class
		"""
		pass
	
		
	##	============================================================
	##						PRIVATE METHODS
	##	============================================================