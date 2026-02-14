export type SourcePlatform = "FACEBOOK" | "YOUTUBE" | "TELEGRAM" | "X";

export interface SourceRecord {
  platform: SourcePlatform;
  sourceUrl: string;
  externalId: string;
  caption?: string;
}

export async function fetchSource(platform: SourcePlatform, sourceUrl: string): Promise<SourceRecord> {
  const externalId = Buffer.from(`${platform}:${sourceUrl}`).toString("base64url");
  return { platform, sourceUrl, externalId, caption: "Fetched from social platform API" };
}
