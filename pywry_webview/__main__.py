from service import Service
from api import RequestResponse, Context


async def joined(id: int, _: Context) -> RequestResponse:
    print("Joined event triggered")
    return RequestResponse(id=id, data={"response": "Joined event triggered"})


async def hello_python(id: int, _: Context) -> RequestResponse:
    print("Hello Python")
    return RequestResponse(id=id, data={"response": "Hello TypeScript"})


def main():
    service = Service(debug=True)
    service.add_event("joined", joined)
    service.add_event("hello_python", hello_python)
    service.run()


if __name__ == "__main__":
    main()
