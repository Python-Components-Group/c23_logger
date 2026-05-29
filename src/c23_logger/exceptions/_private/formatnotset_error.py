class FormatNotSetError(Exception):
	"""
		Represents a (non-exiting) exception that occurs when an operation is called
		that requires a specified format, but no format has been specified.
	"""
	pass