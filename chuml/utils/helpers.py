from flask import request
from chuml.auth import access

def require_argument(argname, default):
	def decorator(func):
		def wrapper(*args,**kwargs):
			argvalue = request.args.get(argname)
			if argvalue != None:
				return func(*args,**kwargs)
			else:
				print("default")
				return default()
		wrapper.__name__ = func.__name__
		return wrapper
	return decorator

