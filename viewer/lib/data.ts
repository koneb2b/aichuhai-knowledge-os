import type { HealthPayload, RulesPayload } from "./types";

let rulesCache: RulesPayload | null = null;
let healthCache: HealthPayload | null = null;

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`${path} 加载失败（HTTP ${response.status}）`);
  }
  return (await response.json()) as T;
}

export async function loadRules(): Promise<RulesPayload> {
  if (rulesCache) return rulesCache;
  const data = await fetchJson<RulesPayload>("/data/rules.json");
  if (data.schema_version !== 1 || !Array.isArray(data.rules)) {
    throw new Error("rules.json 结构不符合 schema_version 1");
  }
  rulesCache = data;
  return data;
}

export async function loadHealth(): Promise<HealthPayload> {
  if (healthCache) return healthCache;
  const data = await fetchJson<HealthPayload>("/data/health.json");
  if (!Array.isArray(data.gates) || typeof data.pass !== "number") {
    throw new Error("health.json 结构不完整");
  }
  healthCache = data;
  return data;
}
