import asyncio

from .base_connection import BaseConnection

class UnixSocketConnection(BaseConnection):
	
	def __init__(self, socket):
		self._socket = socket

	async def setup_connection(self):
		connection = asyncio.open_unix_connection(self._socket)
		reader, writer = await connection
		self._writer = writer
		self.start_read_loop(reader)

	async def start_read_loop(self, reader):
		while True:
			line = await reader.read()
			if line is None or len(line) is 0:
				break
			self.on_data(line)

	async def close_connection(self):
		await self._writer.close()

	async def send(self, buffer):
		if self._writer is not None:
			self._writer.write(buffer)
