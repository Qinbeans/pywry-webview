import type { Writable } from 'svelte/store';
import { writable } from 'svelte/store';
import type { PySession } from './pysession.js';
import type { RequestResponse } from './message.js';

export const labview_session_state: Writable<boolean> = writable(false);
export const py_session_state: Writable<PySession | null> = writable(null);
export const py_response_state: Writable<RequestResponse | null> = writable(null);

export const mock_state: Writable<boolean> = writable(false);