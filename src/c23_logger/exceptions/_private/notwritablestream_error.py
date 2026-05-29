class NotWritableStreamError(Exception):
	"""
		Represents a (non-exiting) exception that occurs when an operation
		is performed that has been provided with a non-writable output stream
		(while it requires a writable one)
	"""
	pass
