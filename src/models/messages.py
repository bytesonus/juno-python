from typing import Union, Any

from ..utils.constants import request_types

class BaseMessage:
    def __init__(self, request_id: str, typ: int):
        self.request_id = request_id
        self.typ = typ


class RegisterModuleRequest(BaseMessage):
    def __init__(self, request_id: str, module_id: str, version: str, dependencies):
        BaseMessage.__init__(
            self,
            request_types.RegisterModuleRequest,
            request_id
        )
        self.module_id = module_id
        self.version = version
        self. dependencies = dependencies


class RegisterModuleResponse(BaseMessage):
    def __init__(self, request_id: str):
        BaseMessage.__init__(
            self,
            request_id,
            request_types.RegisterModuleResponse
        )


class DeclareFunctionRequest(BaseMessage):
    def __init__(self, request_id: str, function: str):
        BaseMessage.__init__(
            self,
            request_id,
            request_types.DeclareFunctionRequest
        )
        self.function = function


class DeclareFunctionResponse(BaseMessage):
    def __init__(self, request_id: str, function: str):
        BaseMessage.__init__(
            self,
            request_id,
            request_types.DeclareFunctionResponse
        )
        self.function = function


class FunctionCallRequest(BaseMessage):
    def __init__(self, request_id: str, function: str, arguments):
        BaseMessage.__init__(
            self,
            request_id,
            request_types.FunctionCallRequest
        )
        self.function = function
        self.arguments = arguments


class FunctionCallResponse(BaseMessage):
    def __init__(self, request_id: str, data):
        BaseMessage.__init__(
            self,
            request_id,
            request_types.FunctionCallResponse
        )
        self.data = data


class RegisterHookRequest(BaseMessage):
    def __init__(self, request_id: str, hook: str):
        BaseMessage.__init__(
            self,
            request_id,
            request_types.RegisterHookRequest
        )
        self.hook = hook


class RegisterHookResponse(BaseMessage):
    def __init__(self, request_id: str):
        BaseMessage.__init__(
            self,
            request_id,
            request_types.RegisterHookResponse
        )


class TriggerHookRequest(BaseMessage):
    def __init__(self, request_id: str, hook: str, data: Any):
        BaseMessage.__init__(
            self,
            request_id,
            request_types.TriggerHookRequest
        )
        self.hook = hook
        self.data = data


class TriggerHookResponse(BaseMessage):
    def __init__(self, request_id: str, hook: str, data):
        BaseMessage.__init__(
            self,
            request_id,
            request_types.TriggerHookResponse
        )
        self.data = data


JunoResponse = Union[
    RegisterModuleResponse,
    RegisterHookResponse,
    TriggerHookResponse,
    DeclareFunctionResponse,
    FunctionCallResponse
]

JunoRequest = Union[
    RegisterModuleRequest,
    DeclareFunctionRequest,
    FunctionCallRequest,
    RegisterHookRequest,
    TriggerHookRequest
]

JunoMessage = Union[
    RegisterModuleResponse,
    RegisterHookResponse,
    TriggerHookResponse,
    DeclareFunctionResponse,
    FunctionCallResponse,
    RegisterModuleRequest,
    DeclareFunctionRequest,
    FunctionCallRequest,
    RegisterHookRequest,
    TriggerHookRequest
]
