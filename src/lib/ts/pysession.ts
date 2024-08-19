import { py_response_state } from './store.js';
import type { Message } from './message.js';

export type PySession = {
	ws: WebSocket;
	send: (message: Message) => void;
	reconnect?: () => void;
	on: (event: string, callback: (params: Record<string, unknown>) => void) => void;
};

export const init_py_session = (url: string): PySession => {
	let ws = new WebSocket(`${url}/api/ws`);
	let is_open = false;
	const listeners: { [key: string]: (params: Record<string, unknown>) => void } = {};

	ws.onopen = () => {
		is_open = true;
	};

	ws.onmessage = (event) => {
		const message = JSON.parse(event.data) as Message;
		if (message.type === 'response') {
			py_response_state.set(message);
		} else if (message.type === 'command') {
			const callback = listeners[message.data.command];
			if (callback) {
				callback(message.data.parameters);
			}
		} else {
			console.error('Unknown message type:', message);
		}
	};

	const send = async (message: Message) => {
		// wait for ws to be open
		if (!is_open) {
			await new Promise((resolve) => {
				const interval = setInterval(() => {
					if (is_open) {
						clearInterval(interval);
						resolve(null);
					}
				}, 100);
			});
		}
		ws.send(JSON.stringify(message));
	};

	const reconnect = () => {
		ws.close();
		ws = new WebSocket(`${url}/api/ws`);
	};

	const on = (event: string, callback: (params: Record<string, unknown>) => void) => {
		listeners[event] = callback;
	};

	return { ws, send, reconnect, on };
};
