"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { DomainSummary, Rule } from "@/lib/types";
import { LEVEL_DOT, LEVEL_TEXT } from "@/lib/levels";

interface RuleExplorerProps {
  rules: Rule[];
  domains: DomainSummary[];
  onOpen: (rule: Rule, trigger: HTMLElement | null) => void;
}

const ENFORCEMENT_OPTIONS = [
  { value: "all", label: "全部" },
  { value: "block", label: "BLOCK" },
  { value: "must", label: "MUST" },
  { value: "should", label: "SHOULD" },
] as const;

type EnforcementFilter = (typeof ENFORCEMENT_OPTIONS)[number]["value"];

function SearchGlyph() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-3.5 w-3.5 shrink-0 text-faint"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
    >
      <circle cx="7" cy="7" r="4.5" />
      <path d="M10.5 10.5 14 14" strokeLinecap="round" />
    </svg>
  );
}

function LockGlyph() {
  return (
    <svg
      role="img"
      aria-label="不可覆盖"
      viewBox="0 0 12 12"
      className="h-2.5 w-2.5 shrink-0 text-faint"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.2"
    >
      <rect x="2.5" y="5.2" width="7" height="5" rx="0.6" />
      <path d="M4.2 5.2V3.9a1.8 1.8 0 0 1 3.6 0v1.3" strokeLinecap="round" />
    </svg>
  );
}

function CheckMark() {
  return (
    <svg
      role="img"
      aria-label="已配置机器检查"
      viewBox="0 0 16 16"
      className="inline h-3 w-3 text-pass/80"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
    >
      <path d="M3 8.5 6.2 11.7 13 5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function RuleExplorer({ rules, domains, onOpen }: RuleExplorerProps) {
  const [domain, setDomain] = useState("all");
  const [enforcement, setEnforcement] = useState<EnforcementFilter>("all");
  const [overridable, setOverridable] = useState("all");
  const [query, setQuery] = useState("");
  const searchRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) {
        return;
      }
      const target = event.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === "INPUT" ||
          target.tagName === "TEXTAREA" ||
          target.tagName === "SELECT" ||
          target.isContentEditable)
      ) {
        return;
      }
      event.preventDefault();
      searchRef.current?.focus();
      searchRef.current?.select();
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const sorted = useMemo(
    () =>
      [...rules].sort(
        (a, b) => b.priority - a.priority || a.id.localeCompare(b.id),
      ),
    [rules],
  );

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return sorted.filter((rule) => {
      if (domain !== "all" && rule.domain !== domain) return false;
      if (enforcement !== "all" && rule.enforcement !== enforcement) return false;
      if (overridable === "yes" && !rule.overridable) return false;
      if (overridable === "no" && rule.overridable) return false;
      if (!needle) return true;
      return [rule.id, rule.rule, rule.doc_id, rule.doc_title]
        .join(" ")
        .toLowerCase()
        .includes(needle);
    });
  }, [sorted, domain, enforcement, overridable, query]);

  const resetFilters = useCallback(() => {
    setDomain("all");
    setEnforcement("all");
    setOverridable("all");
    setQuery("");
  }, []);

  const filtersActive =
    domain !== "all" ||
    enforcement !== "all" ||
    overridable !== "all" ||
    query !== "";

  const counts = useMemo(() => {
    const map: Record<string, number> = { all: rules.length };
    for (const rule of rules) {
      map[rule.enforcement] = (map[rule.enforcement] ?? 0) + 1;
    }
    return map;
  }, [rules]);

  return (
    <section aria-label="规则清单" className="min-w-0">
      <div className="flex items-baseline justify-between gap-4">
        <h2 className="text-[13px] font-medium text-ink">规则清单</h2>
        <p className="font-mono text-[10px] tabular-nums text-faint">
          显示 <span className="text-dim">{filtered.length}</span> / {rules.length}
        </p>
      </div>

      <div className="mt-3 flex flex-wrap items-center gap-x-5 gap-y-3 border-y border-line py-3">
        <label className="flex min-w-[200px] flex-1 items-center gap-2 border-b border-line pb-1.5 focus-within:border-accent/70">
          <span className="sr-only">搜索规则</span>
          <SearchGlyph />
          <input
            ref={searchRef}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Escape") {
                setQuery("");
                event.currentTarget.blur();
              }
            }}
            placeholder="搜索 ID / 规则文本 / 文档"
            className="w-full bg-transparent text-[12px] text-ink outline-none placeholder:text-faint/80"
          />
          {query ? (
            <button
              type="button"
              onClick={() => setQuery("")}
              aria-label="清空搜索"
              className="text-[11px] text-faint transition-colors hover:text-ink"
            >
              ×
            </button>
          ) : (
            <kbd className="font-mono text-[9px] text-faint/80">/</kbd>
          )}
        </label>

        <select
          aria-label="按规则域筛选"
          value={domain}
          onChange={(event) => setDomain(event.target.value)}
          className="bg-transparent text-[11px] text-dim outline-none transition-colors hover:text-ink"
        >
          <option value="all">全部域</option>
          {domains.map((item) => (
            <option key={item.key} value={item.key}>
              {item.key}（{item.count}）
            </option>
          ))}
        </select>

        <select
          aria-label="按可覆盖性筛选"
          value={overridable}
          onChange={(event) => setOverridable(event.target.value)}
          className="bg-transparent text-[11px] text-dim outline-none transition-colors hover:text-ink"
        >
          <option value="all">可覆盖性</option>
          <option value="yes">可覆盖</option>
          <option value="no">不可覆盖</option>
        </select>

        <div role="group" aria-label="按等级筛选" className="flex items-baseline gap-4">
          {ENFORCEMENT_OPTIONS.map((option) => {
            const active = enforcement === option.value;
            return (
              <button
                key={option.value}
                type="button"
                aria-pressed={active}
                onClick={() => setEnforcement(option.value)}
                className={[
                  "flex items-baseline gap-1.5 border-b pb-1 font-mono text-[10px] tracking-[0.04em] transition-colors",
                  active
                    ? "border-accent text-ink"
                    : "border-transparent text-faint hover:text-dim",
                ].join(" ")}
              >
                {option.label}
                <span className="text-[9px] text-faint/80">
                  {counts[option.value] ?? 0}
                </span>
              </button>
            );
          })}
        </div>

        <button
          type="button"
          onClick={resetFilters}
          disabled={!filtersActive}
          className="ml-auto text-[11px] text-faint transition-colors enabled:hover:text-ink disabled:cursor-not-allowed disabled:opacity-40"
        >
          重置
        </button>
      </div>

      {filtered.length === 0 ? (
        <div className="py-16 text-center">
          <p className="text-[12px] text-faint">没有匹配的规则</p>
          <button
            type="button"
            onClick={resetFilters}
            className="mt-3 border-b border-accent/60 pb-0.5 text-[11px] text-dim transition-colors hover:text-ink"
          >
            清除全部筛选
          </button>
        </div>
      ) : (
        <>
          <div className="hidden overflow-x-auto md:block">
            <table className="w-full min-w-[820px] border-collapse text-left">
              <thead>
                <tr className="text-[9px] tracking-[0.14em] text-faint">
                  <th scope="col" className="w-[118px] border-b border-line py-2 pl-3 pr-3 font-normal">
                    规则 ID
                  </th>
                  <th scope="col" className="w-[124px] border-b border-line py-2 pr-3 font-normal">
                    规则域
                  </th>
                  <th scope="col" className="w-[112px] border-b border-line py-2 pr-3 font-normal">
                    等级
                  </th>
                  <th scope="col" className="w-[74px] border-b border-line py-2 pr-3 text-right font-normal">
                    优先级
                  </th>
                  <th scope="col" className="border-b border-line py-2 pr-4 font-normal">
                    规则
                  </th>
                  <th scope="col" className="w-[56px] border-b border-line py-2 text-right font-normal">
                    断言
                  </th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((rule) => (
                  <tr
                    key={rule.id}
                    tabIndex={0}
                    onClick={(event) => onOpen(rule, event.currentTarget)}
                    onKeyDown={(event) => {
                      if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        onOpen(rule, event.currentTarget);
                      }
                    }}
                    aria-label={`查看规则 ${rule.id}`}
                    className="group cursor-pointer border-b border-line/70 transition-colors hover:bg-white/[0.025] focus:outline-none focus-visible:bg-white/[0.04]"
                  >
                    <td className="whitespace-nowrap border-l-2 border-transparent py-2.5 pl-3 pr-3 font-mono text-[11px] text-ink group-hover:border-accent/60">
                      {rule.id}
                    </td>
                    <td className="whitespace-nowrap py-2.5 pr-3 font-mono text-[10px] text-faint">
                      {rule.domain}
                    </td>
                    <td className="whitespace-nowrap py-2.5 pr-3">
                      <span className="inline-flex items-center gap-2">
                        <span
                          aria-hidden="true"
                          className={`h-[5px] w-[5px] ${LEVEL_DOT[rule.enforcement]}`}
                        />
                        <span
                          className={`font-mono text-[10px] tracking-[0.06em] ${LEVEL_TEXT[rule.enforcement]}`}
                        >
                          {rule.enforcement.toUpperCase()}
                        </span>
                        {!rule.overridable ? <LockGlyph /> : null}
                      </span>
                    </td>
                    <td className="whitespace-nowrap py-2.5 pr-3 text-right font-mono text-[11px] tabular-nums text-dim">
                      {rule.priority}
                    </td>
                    <td className="py-2.5 pr-4">
                      <p className="line-clamp-2 text-[12px] leading-snug text-dim transition-colors group-hover:text-ink">
                        {rule.rule}
                      </p>
                    </td>
                    <td className="whitespace-nowrap py-2.5 text-right">
                      {rule.check ? (
                        <CheckMark />
                      ) : (
                        <span className="text-[11px] text-faint/60" title="仅自然语言描述">
                          —
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <ul className="md:hidden">
            {filtered.map((rule) => (
              <li key={rule.id} className="border-b border-line/70">
                <button
                  type="button"
                  onClick={(event) => onOpen(rule, event.currentTarget)}
                  className="block w-full py-3 text-left"
                >
                  <div className="flex items-baseline justify-between gap-3">
                    <span className="font-mono text-[11px] text-ink">{rule.id}</span>
                    <span className="font-mono text-[10px] tabular-nums text-faint">
                      P{rule.priority}
                    </span>
                  </div>
                  <p className="mt-1.5 line-clamp-2 text-[12px] leading-snug text-dim">
                    {rule.rule}
                  </p>
                  <div className="mt-1.5 flex items-center gap-2">
                    <span
                      aria-hidden="true"
                      className={`h-[5px] w-[5px] ${LEVEL_DOT[rule.enforcement]}`}
                    />
                    <span
                      className={`font-mono text-[9px] tracking-[0.06em] ${LEVEL_TEXT[rule.enforcement]}`}
                    >
                      {rule.enforcement.toUpperCase()}
                    </span>
                    <span className="font-mono text-[9px] text-faint">{rule.domain}</span>
                    {!rule.overridable ? <LockGlyph /> : null}
                  </div>
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}
