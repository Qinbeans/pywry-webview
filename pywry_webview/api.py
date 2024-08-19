from uuid import uuid4
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel, Field, TypeAdapter
from queue import Queue
from typing import Callable, Any, Dict, Literal, Optional, Annotated, Union
import asyncio
from enum import IntEnum
from uvicorn import Config, Server


class Status(IntEnum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    UNSUPPORTED_MEDIA_TYPE = 415
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class Context(BaseModel):
    pass


class Message(BaseModel):
    type: Optional[Literal["message"]] = Field(default=None, alias="type")
    id: str = Field(default_factory=lambda: str(uuid4()), alias="id")
    status: int = Field(default=200, alias="status")

    def __str__(self):
        return f"{self.status}"

    def __repr__(self):
        return f"{self.status}"


class CommandData(BaseModel):
    command: str
    parameters: Optional[Dict[str, Any]] = None


class Command(Message):
    type: Literal["command"] = Field(default="command", alias="type")
    data: Optional[CommandData] = Field(default=None, alias="data")

    @property
    def command(self):
        return self.data.command if self.data else None

    @command.setter
    def command(self, value):
        if not self.data:
            self.data = CommandData(command=value)
        else:
            self.data.command = value

    @property
    def parameters(self):
        return self.data.parameters if self.data else None

    @parameters.setter
    def parameters(self, value):
        if not self.data:
            self.data = CommandData(parameters=value)
        else:
            self.data.parameters = value


class ResponseData(BaseModel):
    response: Optional[Union[Dict[str, Any], str]] = None


class RequestResponse(Message):
    type: Literal["response"] = Field(default="response", alias="type")
    data: Optional[ResponseData] = Field(default=None, alias="data")

    @property
    def response(self) -> Optional[Union[Dict[str, Any], str]]:
        if self.status != 200:
            return None
        return self.data.response if self.data else None


MessageDiscriminator = Annotated[
    Union[Command, RequestResponse],
    Field(
        discriminator="type",
    ),
]


class Callback(BaseModel):
    name: str = Field(default="callback", alias="name")
    callback: Callable[[int, Context], RequestResponse] = Field(
        default=None, alias="callback"
    )

    async def __call__(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self.callback):
            return await self.callback(*args, **kwargs)
        else:
            return self.callback(*args, **kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def validate_message_json(data: str) -> MessageDiscriminator:
    type_adaptor: TypeAdapter[Message] = TypeAdapter(MessageDiscriminator)
    return type_adaptor.validate_json(data)


class API:
    def __init__(self, port: int = 5174):
        self.app = FastAPI()
        self.event_adder = Queue()
        self._events: Dict[str, Callback] = {}
        self.context = Context()
        self.port = port

        @self.app.websocket("/api/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            while True:
                while not self.event_adder.empty():
                    event: Callback = self.event_adder.get()
                    self._events[event.name] = event

                try:
                    message = await websocket.receive_text()
                    print(f"Received message: {message}")
                    data = validate_message_json(message)
                    match data.type:
                        case "command":
                            command = data.command
                            if command in self._events:
                                response = await self._events[command](
                                    data.id, self.context
                                )
                                await websocket.send_text(response.model_dump_json())
                            else:
                                error_message = {
                                    "type": "response",
                                    "id": data.id,
                                    "data": {"response": f"Unknown command: {command}"},
                                    "status": Status.NOT_FOUND,
                                }
                                await websocket.send_json(error_message)
                                print(f"Unknown command: {command}")
                        case "response":
                            print(data.response)
                        case _:
                            print("Unknown message type.")
                except Exception as e:
                    print(f"Error during WebSocket communication: {e}")
                    await websocket.close()
                    break
            exit()

    def add_event(self, event: Callback):
        """thread safe event adding"""
        self.event_adder.put(event)

    async def _run_server(self):
        config = Config(app=self.app, host="localhost", port=self.port, loop="asyncio")
        server = Server(config=config)
        await server.serve()

    async def main_loop(self):
        await asyncio.gather(self._run_server())
