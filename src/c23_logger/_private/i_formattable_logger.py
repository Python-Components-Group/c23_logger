from typing import TextIO
from abc import ABC, abstractmethod



class IFormattableLogger(ABC):
	"""
		Represents an object capable of logging, via a text output stream, messages that track
		the steps performed during the execution of a process, optionally in a formatted manner.
        
        Each format string is characterized by the presence or absence of specific placeholders
        to include variable information in the log messages.
		The basic format string defines the following:
        
            - "{message}": The placeholder containing the message provided to the `.log(...)` method
        
        The type of output stream is specified by the descendants of this interface.
        Other format placeholders are specified by the descendants of this interface.

	"""
	
	
	@abstractmethod
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
		pass
	
	
	@abstractmethod
	def log(
			self,
	        message: str,
			format_: bool = True
	):
		"""
			Writes a new message to the specified output stream
            
            Parameters
            ----------
				message: str
                    A string containing the message to log to the output stream
                    
                format_: bool
                    Optional. Default = `True`. A boolean indicating whether to format
                    this message.
                    
            Raises
            ------
                ValueError
                    Occurs if the `message` parameter is an empty string
		"""
		pass


	@abstractmethod
	def set_format(self, format_str: str):
		"""
			Sets a new format string to be used for formatting messages
            that will be logged via this IFormattableLogger
            
            Parameters
            ----------
                format_str: str
                    A string representing the format string that will be used
					to format the next messages that will be logged
            
            Raises
            ------
                InvalidFormatError
                    Occurs if a format containing placeholders different from those acceptable
                    to the descendants of this interface has been provided
		"""
		pass
	
	
	@abstractmethod
	def unset_format(self) -> str:
		"""
			Unsets the previously set format string and returns it. Any message recorded
			after the call to this operation (if not any format has been set again)
			will be logged without any formatting
            
            Returns
            -------
				str
                    A string representing the previously set format string
            
            Raises
            ------
                FormatNotSetError
                    Occurs if no format string is set when this operation is called
		"""
		pass
	
	
	@abstractmethod
	def set_messages_sep(self, new_sep: str):
		"""
			Set a new separator for logging messages
            
            Parameters
            ----------
				new_sep: str
                    A string containing the new separator for logging messages
                    
            Raises
            ------
                ValueError
                    Occurs if the `new_sep` parameter is `None`
		"""
		pass