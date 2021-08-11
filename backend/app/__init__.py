import json

from pkg_resources import resource_string

__version__ = json.loads(resource_string(__name__, '../version.json').decode('utf-8'))
