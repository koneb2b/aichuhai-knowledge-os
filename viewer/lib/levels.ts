import type { Enforcement } from "./types";

export const LEVEL_TEXT: Record<Enforcement, string> = {
  block: "text-fail",
  must: "text-accent",
  should: "text-dim",
  may: "text-faint",
};

export const LEVEL_DOT: Record<Enforcement, string> = {
  block: "bg-fail",
  must: "bg-accent",
  should: "bg-faint",
  may: "bg-faint/50",
};
