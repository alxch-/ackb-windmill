import { REST } from "npm:@discordjs/rest@1.7.1";
import { API } from "npm:@discordjs/core@0.6.0";

type DiscordInteraction = {
  application_id: string;
  token: string;
};

export async function main(
  interaction: DiscordInteraction,
  token: string,
  reply: string
) {
  const rest = new REST({
    version: "10",
  }).setToken(token);
  const api = new API(rest);

  await api.interactions.followUp(
    interaction.application_id,
    interaction.token,
    {
      content: `${reply}`,
    },
  );
}