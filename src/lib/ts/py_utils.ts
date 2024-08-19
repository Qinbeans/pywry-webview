import type { Command, RequestResponse } from './message.js';
import { py_session_state, py_response_state } from './store.js';
import { v4 as uuidv4 } from 'uuid';

export const py_send_session = async (message: Command): Promise<RequestResponse> => {
	py_session_state.update((py_session) => {
		if (py_session === null) {
			throw new Error('py_session is null');
		}
		py_session.send(message);
		return py_session;
	});
	// wait for py_response_state to be updated
	return new Promise((resolve) => {
		const unsubscribe = py_response_state.subscribe((response) => {
			if (response && response.id === message.id) {
				resolve(response);
				unsubscribe();
			}
		});
	});
};

export const py_add_listener = (
	command: string,
	callback: (params: Record<string, unknown>) => void
) => {
	py_session_state.update((py_session) => {
		if (py_session === null) {
			throw new Error('py_session is null');
		}
		py_session.on(command, callback);
		return py_session;
	});
};

export const new_command = (command: string, parameters: Record<string, unknown>): Command => {
	return {
		type: 'command',
		id: uuidv4(),
		data: {
			command,
			parameters
		},
		status: 0
	};
};
