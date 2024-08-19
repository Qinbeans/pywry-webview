import sys
from typing import Tuple, Callable
from pathlib import Path
from pywry_webview.api import Api, Callback, Context
from pywry import PyWry


class Service:
    def __init__(
        self,
        window_name: str = "PyWry Window",
        window_size: Tuple[int, int] = (1200, 800),
        debug: bool = False,
        path_or_url: str = "http://localhost:5173",
    ):
        self.window_name = window_name
        self.window_size = window_size
        self.handler = PyWry()
        self.path_or_url: str | Path = path_or_url
        if isinstance(path_or_url, Path):
            self.api = Api(path=path_or_url)
            self.path_or_url = "http://localhost:5174"
        else:
            self.api = Api()
        self.debug = debug

    @property
    def _script(self):
        return f"""
        <script>
            window.location.replace("{self.path_or_url}");
        </script>
        """

    def add_event(self, event: str, callback_fn: Callable[[int, Api, Context], None]):
        self.api.add_event(Callback(name=event, callback=callback_fn))

    def run(self):
        try:
            outgoing = dict(
                width=self.window_size[0],
                height=self.window_size[1],
                title=self.window_name,
                html=self._script,
            )
            print(f"Outgoing: {outgoing}")
            self.handler.send_outgoing(outgoing)
            self.handler.start(debug=self.debug)
            self.handler.loop.run_until_complete(self.api.main_loop())
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Shutting down gracefully...")
            self.handler.close()
            sys.exit(0)
