from typing import Callable
import asyncio
import abc


class BaseConnection(object):

    @abc.abstractmethod
    async def setup_connection(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def close_connection(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, request: bytes):
        raise NotImplementedError

    def set_on_data_listener(self, on_data_handler: Callable[[bytes], None]):
        self.on_data_handler = on_data_handler

    def on_data(self, buffer):
        if self.on_data_handler is not None:
            asyncio.create_task(self.on_data_handler(buffer))
