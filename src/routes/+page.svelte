<script lang="ts">
	import { mock_state } from '$lib/ts/store';
	import { py_send_session, new_command } from '$lib/ts/py_utils';

	let message: string | undefined;

	const click_me = async () => {
		try {
			const response = await py_send_session(new_command('hello_python', {}));
			if (response.status !== 200) {
				message = `Error: ${response.status}`;
				throw new Error(message);
			}
			if (typeof response.data.response === 'string') {
				message = response.data.response;
			} else {
				message = JSON.stringify(response.data.response);
			}
			console.log(response);
		} catch (error) {
			console.error(error);
		}
	};

	const change_state_py = async () => {
		try {
			const response = await py_send_session(new_command('trigger_state_change', {}));
			if (response.status !== 200) {
				message = `Error: ${response.status}`;
				throw new Error(message);
			}
			if (typeof response.data.response === 'string') {
				message = response.data.response;
			} else {
				message = JSON.stringify(response.data.response);
			}
			console.log(response);
		} catch (error) {
			console.error(error);
		}
	};

	const clear_message = () => {
		message = undefined;
	};
</script>

<main class="bg-black">
	<button
		on:click={click_me}
		class="bg-gray-500 hover:bg-yellow-300 transition duration-500 rounded-full px-2 py-1 w-fit m-2"
		>Hello Python!</button
	>
	{#if message}
		<p>{message}</p>
		<button
			on:click={clear_message}
			class="bg-gray-500 hover:bg-yellow-300 transition duration-500 rounded-full px-2 py-1 w-fit m-2"
			>Clear</button
		>
	{/if}
	<button
		on:click={change_state_py}
		class="bg-gray-500 hover:bg-yellow-300 transition duration-500 rounded-full px-2 py-1 w-fit m-2"
		>Change State</button
	>
	{#if $mock_state}
		<p>State is true</p>
	{/if}
	{#if !$mock_state}
		<p>State is false</p>
	{/if}
</main>
