from typing import Dict, Callable, Any
import ipaddress
import asyncio

from .connection.base_connection import BaseConnection
from .connection.unix_socket_connection import UnixSocketConnection
from .connection.inet_socket_connection import InetSocketConnection
from .protocol.base_protocol import BaseProtocol

from .models.messages import JunoRequest, FunctionCallResponse

from .utils.constants import request_types

class JunoModule(object):

	def __init__(self, connection: BaseConnection, protocol: BaseProtocol):
		self.protocol = protocol
		self.connection = connection
		self.functions = dict()
		self.hook_listeners = dict()
		self.registered = False
		self.message_buffer = []
		self.requests = dict()

	@staticmethod
	def default(socket_path: str):
		try:
			parts = socket_path.split(':')
			host = ipaddress.ip_address(parts[0])
			port = int(parts[1])
			return JunoModule.from_inet_socket(host, port)
		except:
			return JunoModule.from_unix_socket(socket_path)

	@staticmethod
	def from_unix_socket(socket_path: str):
		return JunoModule(UnixSocketConnection(socket_path), BaseProtocol.default())

	@staticmethod
	def from_inet_socket(host: str, port: int):
		return JunoModule(InetSocketConnection(host, port), BaseProtocol.default())

	async def initialize(self, module_id: str, version: str, dependencies: Dict[str, str]):
		self.module_id = module_id
		self.connection.set_on_data_listener(self.on_data_handler)
		await self.connection.setup_connection()
		await self._send_request(
			self.protocol.initialize(module_id, version, dependencies)
		)

	async def declare_function(self, fn_name: str, fn: Callable[[Dict[str, Any]], Any]):
		self.functions[fn_name] = fn
		await self._send_request(self.protocol.declare_function(fn_name))

	async def call_function(self, fn_name: str, args: Dict[str, Any]) -> Any:
		return await self._send_request(self.protocol.call_function(fn_name, args))
	
	async def register_hook(self, hook: str, fn: Callable[[Any], None]):
		self.hook_listeners[hook] = fn
		await self._send_request(self.protocol.register_hook(hook))
	
	async def trigger_hook(self, hook: str, data: Any):
		await self._send_request(self.protocol.trigger_hook(hook, data))

	async def close(self):
		await self.connection.close_connection()
	
	async def _send_request(self, req: JunoRequest):
		if req.typ is request_types.RegisterModuleRequest and self.registered:
			raise EnvironmentError('Module already registered')

		encoded = self.protocol.encode(req)
		if self.registered or req.typ is request_types.RegisterModuleRequest:
			await self.connection.send(encoded)
		else:
			self.message_buffer.extend(encoded)
		
		task = asyncio.create_task(lambda: asyncio.get_running_loop().run_forever())
		self.requests[req.request_id] = task
		return task

	async def on_data_handler(self, data: bytes):
		response = self.protocol.decode(data)
		switcher = {
			request_types.RegisterModuleResponse: lambda: True,
			request_types.FunctionCallResponse: lambda: response.data,
			request_types.DeclareFunctionResponse: lambda: True,
			request_types.RegisterHookResponse: lambda: True,
			request_types.TriggerHookRequest: lambda: self.execute_hook_triggered(response),
			request_types.FunctionCallRequest: lambda: self.execute_function_call(response),
		}
		func = switcher.get(response.typ, lambda: False)
		value = func()

		if type(value) == asyncio.Task:
			value = await value

		if self.requests[response.request_id]:
			self.requests[response.request_id].set_result(value)
			del(self.requests[response.request_id])

	async def execute_function_call(self, request: JunoRequest) -> Any:
		if self.functions[request.function]:
			response = self.functions[request.function](request.arguments)
			if type(response) == asyncio.Task:
				response = await response
			self._send_request(FunctionCallResponse(request.request_id, response))
			return True
		else:
			return False

	async def execute_hook_triggered(self, req: JunoRequest):
		if req.hook:
			if req.hook == 'juno.activated':
				self.registered = True
				if len(self.message_buffer) > 0:
					await self.connection.send(self.message_buffer)
					self.message_buffer.clear()
			elif self.hook_listeners[req.hook]:
				for listener in self.hook_listeners[req.hook]:
					listener(req.data)
				return True
			else:
				return False
		else:
			return False

if __name__ == "__main__":
	module = JunoModule.from_unix_socket('/home/rakshith/Projects/juno/juno.sock')
	module.initialize("test", "1.0.0", None)
	