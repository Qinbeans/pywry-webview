dev:
    pnpm run dev &
    python pywry_webview

install:
    pnpm install
    python -m pip install git+https://github.com/JKISoftware/wrypy
    python -m pip install -e .[dev]

build:
    pnpm run build
    python -m nuitka --onefile --include-data-dir=build=build ./pywry_webview/deploy.py --output-filename=pywry_webview

# test:

update:
    pnpm update
    python -m pip install -e .[dev]

format:
    pnpm run format
    python -m ruff format

lint:
    pnpm run lint
    python -m ruff check