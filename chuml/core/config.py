import yaml
import sys

_self = sys.modules[__name__]

with open("../config.txt", 'r') as stream:
    try:
        _data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for k, v in _data.items():
	setattr(_self, k, v)
