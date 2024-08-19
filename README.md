# Pywry Webview

A full example of a webview application with a communication between Python and JavaScript/Typescript. This project demonstrates how to use Pywry aswell as how to setup a state management system with websockets and Sveltekit stores.

<img src="./docs/pywry-webview.png" alt="Pywry Webview" width="75%">

This implementation with Websockets should allow for bi-directional communication between the Python backend and the frontend. This is useful for real-time applications or applications that require a lot of data to be sent back and forth.

## Demo

<video width="75%" controls>
  <source src="./docs/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Requirements

- Python 3.12+
- PNPM 8.15+
- Just 1.32+

## Installation

```bash
just install
```

## Usage

```bash
just dev
```

## Build

```bash
just build
```

Things like `test` are WIP.
