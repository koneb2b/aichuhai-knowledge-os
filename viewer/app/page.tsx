"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { DomainLedger } from "@/components/domain-ledger";
import { GatesPanel } from "@/components/gates-panel";
import { LedgerStrip } from "@/components/ledger-strip";
import { RuleDrawer } from "@/components/rule-drawer";
import { RuleExplorer } from "@/components/rule-explorer";
import { RuleStrip } from "@/components/rule-strip";
import { MobileNav, Sidebar } from "@/components/sidebar";
import { loadHealth, loadRules } from "@/lib/data";
import type { Rule, ViewerData } from "@/lib/types";

function formatTime(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleString("zh-CN", { hour12: false });
}

function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen lg:flex">
      <Sidebar />
      <main className="min-w-0 flex-1">
        <MobileNav />
        <div className="mx-auto max-w-[1360px] px-5 py-7 sm:px-8 lg:px-10 lg:py-9">
          {children}
        </div>
      </main>
    </div>
  );
}

function LoadingState() {
  return (
    <Shell>
      <div
        className="animate-pulse space-y-9"
        aria-busy="true"
        aria-label="正在加载数据快照"
      >
        <div className="space-y-3">
          <div className="h-2.5 w-44 bg-white/[0.06]" />
          <div className="h-6 w-56 bg-white/[0.06]" />
          <div className="h-2.5 w-72 bg-white/[0.04]" />
        </div>
        <div className="grid grid-cols-2 gap-px border-y border-line bg-line sm:grid-cols-3 xl:grid-cols-6">
          {Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="h-20 bg-base" />
          ))}
        </div>
        <div className="h-14 bg-white/[0.03]" />
        <div className="grid gap-8 xl:grid-cols-[minmax(0,1fr)_316px]">
          <div className="h-96 bg-white/[0.03]" />
          <div className="h-72 bg-white/[0.03]" />
        </div>
      </div>
    </Shell>
  );
}

function ErrorState({ message }: { message: string }) {
  return (
    <Shell>
      <div className="max-w-xl border-l-2 border-fail pl-5">
        <p className="text-[9px] tracking-[0.2em] text-faint">SNAPSHOT ERROR</p>
        <h1 className="mt-2 text-[15px] text-fail">数据快照加载失败</h1>
        <p className="mt-2 break-words text-[12px] leading-relaxed text-dim">
          {message}
        </p>
        <p className="mt-7 text-[9px] tracking-[0.14em] text-faint">
          在仓库根目录运行后刷新
        </p>
        <code className="mt-2 block border-l border-line-strong pl-3 font-mono text-[11px] text-ink">
          python Knowledge-OS/tools/viewer_data.py
        </code>
      </div>
    </Shell>
  );
}

export default function Page() {
  const [data, setData] = useState<ViewerData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<Rule | null>(null);
  const openerRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([loadRules(), loadHealth()])
      .then(([rules, health]) => {
        if (!cancelled) setData({ rules, health });
      })
      .catch((reason: unknown) => {
        if (!cancelled) {
          setError(reason instanceof Error ? reason.message : String(reason));
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const openRule = useCallback((rule: Rule, trigger: HTMLElement | null) => {
    openerRef.current = trigger;
    setSelected(rule);
  }, []);

  const closeRule = useCallback(() => {
    setSelected(null);
    openerRef.current?.focus();
    openerRef.current = null;
  }, []);

  if (error) return <ErrorState message={error} />;
  if (!data) return <LoadingState />;

  const { rules, health } = data;
  const blockCount = rules.rules.filter(
    (rule) => rule.enforcement === "block",
  ).length;
  const lockedCount = rules.rules.filter((rule) => !rule.overridable).length;
  const checkCount = rules.rules.filter((rule) => rule.check).length;
  const allPassed = health.fail === 0;
  const snapshotDrift =
    health.summary.rules_version !== rules.rules_version;

  return (
    <Shell>
      <header className="flex flex-wrap items-start justify-between gap-x-10 gap-y-4">
        <div className="min-w-0">
          <p className="text-[9px] tracking-[0.22em] text-faint">
            KNOWLEDGE-OS · CONTRACT
          </p>
          <h1 className="mt-2 text-[21px] font-medium leading-none tracking-[-0.01em] text-ink">
            规则契约
          </h1>
          <p className="mt-2 text-[12px] text-dim">
            {rules.total_rules} 条规则 · {rules.domains.length} 个规则域 ·{" "}
            <span className="font-mono text-[11px] text-faint">
              {rules.rules_version}
            </span>
          </p>
        </div>

        <div className="text-right">
          <p className="flex items-center justify-end gap-2 text-[12px]">
            <span
              aria-hidden="true"
              className={`h-[5px] w-[5px] ${allPassed ? "bg-pass" : "bg-fail"}`}
            />
            <span className="font-mono tabular-nums text-ink">
              {health.pass}
              <span className="text-faint">/{health.pass + health.fail}</span>
            </span>
            <span className="text-dim">闸门通过</span>
          </p>
          <p className="mt-1.5 font-mono text-[10px] text-faint">
            快照 {formatTime(health.generated_at)}
          </p>
          <p className="mt-0.5 text-[10px] text-faint">只读 · 无账号 · 无数据库</p>
        </div>
      </header>

      <div className="mt-8 space-y-9">
        {snapshotDrift ? (
          <p
            role="status"
            className="border-l-2 border-fail bg-fail/[0.06] px-4 py-2.5 text-[11px] leading-relaxed text-fail"
          >
            快照版本 {health.summary.rules_version} 与规则版本{" "}
            {rules.rules_version} 不一致，请重跑 viewer_data.py。
          </p>
        ) : null}

        <LedgerStrip
          total={rules.total_rules}
          domains={rules.domains.length}
          block={blockCount}
          locked={lockedCount}
          checks={checkCount}
          artifacts={health.summary.artifacts}
        />

        <RuleStrip rules={rules.rules} onOpen={openRule} />

        <div className="grid gap-9 xl:grid-cols-[minmax(0,1fr)_316px] xl:gap-10">
          <RuleExplorer
            rules={rules.rules}
            domains={rules.domains}
            onOpen={openRule}
          />

          <div className="space-y-9 xl:sticky xl:top-8 xl:self-start">
            <DomainLedger domains={rules.domains} />
            <GatesPanel gates={health.gates} />
          </div>
        </div>

        <footer className="flex flex-wrap items-baseline justify-between gap-3 border-t border-line pt-5 text-[10px] text-faint">
          <p>只读快照，不改任何源文件。改规则请改 SOP 后重跑编译。</p>
          <code className="font-mono text-dim">
            python Knowledge-OS/tools/viewer_data.py
          </code>
        </footer>
      </div>

      {selected ? <RuleDrawer rule={selected} onClose={closeRule} /> : null}
    </Shell>
  );
}
