import json

from .base_protocol import BaseProtocol

class JsonProtocol(BaseProtocol):
	
	def encode(self, req):
		return bytes(json.dumps(req), 'utf-8')
	
	def decode(self, req):
		return json.loads(req.decode())
