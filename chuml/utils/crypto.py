import hashlib
import base64
from flask import request
from secrets import token_bytes

if __name__ == "__main__":
	seed = "blablabla"
else:
	from chuml.utils import db
	seed = db.load_or_write("sensitive", "app_secret")

sha256 = lambda m: hashlib.sha256(m.encode('utf-8')).digest()
b64encode = base64.urlsafe_b64encode
b64decode = base64.urlsafe_b64decode

b58string = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
def b58encode(b):
	num = int.from_bytes(b, byteorder="big")
	if num == 0:
		return b58string[0]
	arr = []
	while num:
		num, rem = divmod(num, 58)
		arr.append(b58string[rem])
		
	return "".join(arr)

sum_check_char = lambda x : b58string[sum(b58string.index(c)*pow(3,i,58) for i,c in enumerate(x)) % 58]
add_sum_check = lambda x : x + sum_check_char(x)
check = lambda x : x[-1] == sum_check_char(x[:-1])

"""
def b58decode(x):
	num = 0
	for i, s in enumerate(x):
		num += 58**i * b58string.index(s)
	return num.to_bytes(byteorder="big", length=(num.bit_length() + 7) // 8)
"""

def H(x):
	y = b58encode(sha256(x))
	#padding
	if len(y) < 32:
		y += (32 - len(y))*b58string[0]
	return add_sum_check(y)

derive_secret = lambda m: H(seed + m)

get_iid        = lambda x : b58encode(sha256(x))[:12]
get_random_iid = lambda   : b58encode(token_bytes(32))[:12]
 
def require_secret(secret):
	def decorator(func):
		def wrapper(*args,**kwargs):
			s = request.args.get("secret", default="")
			if not s == secret:
				return "Not Authorized. Secret required."
			else:
				return func(*args, **kwargs)
		wrapper.__name__ = func.__name__
		return wrapper
	return decorator

if __name__ == "__main__":
	s = derive_secret("crypto")
	print("secret:", s)
	print(" check:", check(s))
	print("iid:", get_iid("cccarypto"))


