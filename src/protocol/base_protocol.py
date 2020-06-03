from typing import Dict, Any
import time
import abc

from ..models.messages import RegisterModuleRequest, DeclareFunctionRequest
from ..models.messages import FunctionCallRequest, RegisterHookRequest
from ..models.messages import TriggerHookRequest, JunoMessage
from .json_protocol import JsonProtocol


class BaseProtocol(object):
    def __init__(self):
        pass

    @classmethod
    def default(cls):
        return JsonProtocol()

    def _generate_request_id(self):
        return self.module_id + str(time.time_ns())

    def get_module_id(self):
        return self.module_id

    def set_module_id(self, module_id):
        self.module_id = module_id

    def initialize(self, module_id: str, version: str, dependencies: Dict[str, str]):
        self.module_id = module_id
        return RegisterModuleRequest(self._generate_request_id(), module_id, version, dependencies)

    def register_hook(self, hook: str) -> RegisterHookRequest:
        return RegisterHookRequest(self._generate_request_id(), hook)

    def trigger_hook(self, hook: str, data: Any) -> TriggerHookRequest:
        return TriggerHookRequest(self._generate_request_id(), hook, data)

    def declare_function(self, function: str) -> DeclareFunctionRequest:
        return DeclareFunctionRequest(self._generate_request_id(), function)

    def call_function(self, function: str, args: Dict[str, Any]) -> FunctionCallRequest:
        return FunctionCallRequest(self._generate_request_id(), function, args)

    @abc.abstractmethod
    def encode(self, req: JunoMessage):
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, data) -> JunoMessage:
        raise NotImplementedError
