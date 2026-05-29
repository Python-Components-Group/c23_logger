from typing import TextIO, Set, Dict
from abc import abstractmethod
from ._a_base_formlogger import _ABaseFormattableLogger

from datetime import datetime as DateTime

from ..exceptions import InvalidFormatError



class ATemporalFormattLogger(_ABaseFormattableLogger):
	"""
		Represents an `IFormattLogger` that logs, along with the provided messages,
        the date associated with the message's logging.
        
        The specific format placeholders implemented are as follows:
            
            - {day}: A placeholder that is populated with the current day of the month
			- {month}: A placeholder that is set to the current month number
            - {year}: A placeholder that is set to the current year number
            - {hour}: A placeholder that is set to the current hour
            - {min}: A placeholder that is set to the minutes elapsed since the start of the current hour
			- {second}: Placeholder that is populated with the seconds elapsed since the start of the current minute

		The type of output stream used is specified by the descendants of this abstract class.
		The other placeholders in the format are specified by the descendants of this abstract class.
	"""
	
	_DATE_PLACEHS: Set[str] = {
		"day", "month", "year",
		"hour", "min", "second"
	}
	
	def __init__(
			self,
			stream: TextIO
	):
		"""
			Creates a new `ATemporalFormattLogger` and associates it with the provided
			output stream
            
            Parameters
            ----------
				stream: TextIO
                    A `TextIO` object representing the first output stream to be associated
                    with this logger
                    
            Raises
            ------
				NotWritableStreamError
                    Occurs if the provided stream is not writable (and therefore an output stream)
            
                InvalidStreamTypeError
                    Occurs if the provided stream is of an invalid type with respect to the stream type
                    specified by the descendants of this abstract class
		"""
		super().__init__(stream)
	
	
	##	============================================================
	##						ABSTRACT METHODS
	##	============================================================
	
	
	@abstractmethod
	def _ap__assert_stream_type(self, stream: TextIO):
		pass
	
	
	##	============================================================
	##						PRIVATE METHODS
	##	============================================================


	def _ap__assert_format(self, placehs: Set[str]):
		extra_fields: Set[str] = (
			placehs.difference(self._DATE_PLACEHS).union(
			self._DATE_PLACEHS.difference(placehs))
		)
		if extra_fields != set():
			raise InvalidFormatError()
		
		self._curr_placehs = placehs
	
	
	def _ap__format_vars(self) -> Dict[str, str]:
		placehs: Dict[str, str] = dict()
		if len(self._curr_placehs) == 0:
			return placehs
		
		datenow: DateTime = DateTime.now()
		if "day" in self._curr_placehs:
			placehs["day"] = str(datenow.day).zfill(2)
		if "month" in self._curr_placehs:
			placehs["month"] = str(datenow.month).zfill(2)
		if "year" in self._curr_placehs:
			placehs["year"] = str(datenow.year).zfill(2)
		if "hour" in self._curr_placehs:
			placehs["hour"] = str(datenow.hour).zfill(2)
		if "min" in self._curr_placehs:
			placehs["min"] = str(datenow.minute).zfill(2)
		if "second" in self._curr_placehs:
			placehs["second"] = str(datenow.second).zfill(2)
			
		return placehs