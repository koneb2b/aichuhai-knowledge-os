export type Enforcement = "block" | "must" | "should" | "may";

export type CheckType = "grep" | "ast" | "file" | "config" | "manual";

export interface RuleCheck {
  type: CheckType;
  target: string;
  assertion: string;
  mode?: "present" | "absent";
  pattern?: string;
  exclude?: string[];
}

export interface Rule {
  id: string;
  domain: string;
  doc_id: string;
  doc_title: string;
  version: string;
  priority: number;
  enforcement: Enforcement;
  overridable: boolean;
  rule: string;
  check: RuleCheck | null;
  source: string;
}

export interface DomainSummary {
  key: string;
  title: string;
  count: number;
}

export interface RulesPayload {
  schema_version: number;
  rules_version: string;
  total_rules: number;
  domains: DomainSummary[];
  rules: Rule[];
}

export interface Gate {
  name: string;
  ok: boolean;
  detail: string;
  group: string;
}

export interface HealthSummary {
  total_rules: number;
  domains: number;
  rules_version: string;
  artifacts: number;
  pass: number;
  fail: number;
}

export interface HealthPayload {
  generated_at: string;
  exit_code: number;
  pass: number;
  fail: number;
  summary: HealthSummary;
  gates: Gate[];
}

export interface ViewerData {
  rules: RulesPayload;
  health: HealthPayload;
}
