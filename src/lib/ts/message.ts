export type Command = {
	type: 'command';
	id: string;
	data: {
		command: string;
		parameters: Record<string, unknown>;
	};
	status: number;
};

export type ResponseData = Record<string, unknown> | string;

export type RequestResponse = {
	type: 'response';
	id: string;
	data: {
		response: ResponseData | undefined;
	};
	status: number;
};

export type Message = Command | RequestResponse;
