export async function main(interaction: any) {
  return interaction?.data?.options?.[0]?.value ?? "No question asked";
}