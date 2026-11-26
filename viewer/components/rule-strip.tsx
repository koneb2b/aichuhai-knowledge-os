"use client";

import type { Rule } from "@/lib/types";

const TICK_COLOR: Record<Rule["enforcement"], string> = {
  block: "bg-fail",
  must: "bg-accent",
  should: "bg-faint",
  may: "bg-faint/60",
};

const LEGEND: Array<{ label: string; swatch: string }> = [
  { label: "BLOCK", swatch: "bg-fail" },
  { label: "MUST", swatch: "bg-accent" },
  { label: "SHOULD", swatch: "bg-faint" },
];

interface RuleStripProps {
  rules: Rule[];
  onOpen: (rule: Rule, trigger: HTMLElement | null) => void;
}

export function RuleStrip({ rules, onOpen }: RuleStripProps) {
  const ordered = [...rules].sort(
    (a, b) => b.priority - a.priority || a.id.localeCompare(b.id),
  );
  const max = Math.max(1, ...ordered.map((rule) => rule.priority));

  return (
    <section aria-label="规则密度">
      <div className="flex flex-wrap items-baseline justify-between gap-3">
        <div className="flex items-baseline gap-3">
          <h2 className="text-[10px] tracking-[0.16em] text-faint">规则密度</h2>
          <p className="text-[10px] text-faint">
            按优先级降序 · 点击刻度查看
          </p>
        </div>
        <div className="flex items-center gap-4">
          {LEGEND.map((item) => (
            <span key={item.label} className="flex items-center gap-1.5">
              <span aria-hidden="true" className={`h-[3px] w-[9px] ${item.swatch}`} />
              <span className="font-mono text-[9px] tracking-[0.08em] text-faint">
                {item.label}
              </span>
            </span>
          ))}
        </div>
      </div>

      <div className="mt-3 flex h-11 items-end gap-1 border-b border-line">
        {ordered.map((rule) => {
          const height = 8 + Math.round((rule.priority / max) * 28);
          return (
            <button
              key={rule.id}
              type="button"
              onClick={(event) => onOpen(rule, event.currentTarget)}
              title={`${rule.id} · ${rule.enforcement.toUpperCase()} · P${rule.priority}`}
              aria-label={`打开规则 ${rule.id}`}
              style={{ height }}
              className={`w-[6px] shrink-0 opacity-70 transition-opacity hover:opacity-100 ${TICK_COLOR[rule.enforcement]}`}
            />
          );
        })}
      </div>
    </section>
  );
}
