import { type Resource } from 'https://deno.land/x/windmill@v1.108.0/mod.ts';

import {
	InteractionResponseType,
	InteractionType,
	verifyKey
} from 'npm:discord-interactions@4.4.0';

type DiscordInteraction = {
	id: string;
	token: string;
	type: InteractionType;
};

export async function main(
	x_signature_ed25519: string,
	x_signature_timestamp: string,
	raw_string: string,
	discord_config: Resource<'c_discord_bot'>
) {
	const interaction: DiscordInteraction = JSON.parse(raw_string);

	// We'll need the http request body as a string and the two headers to verify the request signature
	// https://discord.com/developers/docs/interactions/receiving-and-responding#security-and-authorization
	const isVerified = await verifyKey(
		raw_string,
		x_signature_ed25519,
		x_signature_timestamp,
		discord_config.public_key
	);

	if (!isVerified) {
		throw new Error('The request signature is not valid');
	}

	// If we get a PING, we need to respond with a PONG
	const type = interaction.type as InteractionType;
	if (type === InteractionType.PING) {
		return { type: InteractionResponseType.PONG };
	}

	return { type: InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
  interaction: interaction };
}