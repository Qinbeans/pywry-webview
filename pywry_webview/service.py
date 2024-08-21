import sys
from typing import Tuple, Callable, Optional
from pathlib import Path
from pywry_webview.api import Api, Callback, Context
from wrypy.wrypy import WebViewWindow
from wrypy.models import WebViewConfig, WebViewOnOffOptions, WebViewPosition, WebViewSize
import asyncio
import threading
import time

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
        self.handler: Optional[WebViewWindow] = None
        self.path_or_url: str | Path = path_or_url
        if isinstance(path_or_url, Path):
            self.api = Api(path=path_or_url)
            self.path_or_url = "http://localhost:5174"
        else:
            self.api = Api()
        self.debug = debug

    def add_event(self, event: str, callback_fn: Callable[[int, Api, Context], None]):
        self.api.add_event(Callback(name=event, callback=callback_fn))

    def run(self):
        try:
            self.handler = WebViewWindow(
                WebViewConfig(
                    title=self.window_name,
                    url=self.path_or_url,
                    size=WebViewSize(width=self.window_size[0], height=self.window_size[1]),
                    position=WebViewPosition(x=0, y=0),
                    on_off=WebViewOnOffOptions(
                        debug=self.debug,
                    ),
                ).model_dump_json()
            )
            
            loop_thread = threading.Thread(target=lambda: asyncio.run(self.api.main_loop()))
            loop_thread.start()

            while self.handler.is_running():
                print("Running...")
                time.sleep(1)

        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Shutting down gracefully...")
            self.handler.close()
            sys.exit(0)
