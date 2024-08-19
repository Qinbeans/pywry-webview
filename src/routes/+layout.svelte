<script lang="ts">
	import '$lib/styles/app.css';
	import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import { py_session_state, mock_state } from '$lib/ts/store';
	import { init_py_session } from '$lib/ts/pysession';
	import { py_send_session, new_command, py_add_listener } from '$lib/ts/py_utils';

	py_session_state.set(init_py_session('http://localhost:5174'));
	storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });
	py_send_session(new_command('joined', {}));
	py_add_listener('trigger_state_change', () => {
		console.log('trigger_state_change');
		mock_state.update((state) => {
			// if false, return true
			if (!state) {
				return !state;
			}
			return state;
		});
	});
</script>

<div class="h-dvh w-dvw bg-black">
	<slot />
</div>
