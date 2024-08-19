dev:
    pnpm run dev &
    python pywry_webview

install:
    pnpm install
    python -m pip install -e .[dev]

# build:

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