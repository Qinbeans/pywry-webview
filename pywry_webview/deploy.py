from pathlib import Path
from pywry_webview.service import Service
from pywry_webview.api import Api, Context, RequestResponse
from uuid import uuid4

async def joined(id: int, _api: Api, _ctx: Context) -> RequestResponse:
    print("Joined event triggered")
    return RequestResponse(id=id, data={"response": "Joined event triggered"})


async def hello_python(id: int, _api: Api, _ctx: Context) -> RequestResponse:
    print("Hello Python")
    return RequestResponse(id=id, data={"response": "Hello TypeScript"})


async def trigger_state_change(id: int, api: Api, _ctx: Context) -> RequestResponse:
    api.send_event(
        "trigger_state_change", str(uuid4()), {"state": "changed"}
    )  # No await needed as messages are queued
    return RequestResponse(id=id, data={"response": "State change triggered"})


def main():
    service = Service(path_or_url=Path(__file__).parent / "build" / "index.html")
    service.add_event("joined", joined)
    service.add_event("hello_python", hello_python)
    service.add_event("trigger_state_change", trigger_state_change)
    service.run()


if __name__ == "__main__":
    main()