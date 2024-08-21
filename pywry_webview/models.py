"""
Python bridge classes for Rust objects
"""

from typing import Optional
from pydantic import BaseModel
from enum import IntEnum

class WebViewFullscreen(IntEnum):
    None_ = 0
    Exclusive = 1
    Borderless = 2


class WebViewOnOffOptions(BaseModel):
    resizable: Optional[bool] = None
    debug: Optional[bool] = None
    devtools: Optional[bool] = None
    maximized: Optional[bool] = None
    minimizable: Optional[bool] = None
    maximizable: Optional[bool] = None
    closable: Optional[bool] = None
    visible: Optional[bool] = None
    decorations: Optional[bool] = None
    always_on_top: Optional[bool] = None

class WebViewPosition(BaseModel):
    x: int = 0
    y: int = 0

class WebViewSize(BaseModel):
    width: int
    height: int

class WebViewConfig(BaseModel):
    url: str
    size: Optional[WebViewSize] = None
    title: Optional[str] = None
    icon_path: Optional[str] = None
    max_size: Optional[WebViewSize] = None
    min_size: Optional[WebViewSize] = None
    position: Optional[WebViewPosition] = None
    fullscreen: Optional[WebViewFullscreen] = None
    on_off_options: Optional[WebViewOnOffOptions] = None