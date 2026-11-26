"use client";

import { useEffect, useRef, useState } from "react";
import type { Rule } from "@/lib/types";
import { LEVEL_TEXT } from "@/lib/levels";

interface RuleDrawerProps {
  rule: Rule;
  onClose: () => void;
}

function CloseGlyph() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-3.5 w-3.5"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
    >
      <path d="M4 4l8 8M12 4l-8 8" strokeLinecap="round" />
    </svg>
  );
}

function Field({
  label,
  value,
  mono = false,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div className="min-w-0">
      <dt className="text-[9px] tracking-[0.12em] text-faint">{label}</dt>
      <dd
        className={`mt-1.5 break-words text-[12px] text-dim ${
          mono ? "font-mono text-[11px]" : "leading-relaxed"
        }`}
      >
        {value}
      </dd>
    </div>
  );
}

export function RuleDrawer({ rule, onClose }: RuleDrawerProps) {
  const panelRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const [copied, setCopied] = useState<"id" | "source" | null>(null);

  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    closeRef.current?.focus();

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
        return;
      }
      if (event.key !== "Tab") return;

      const root = panelRef.current;
      if (!root) return;
      const focusable = Array.from(
        root.querySelectorAll<HTMLElement>(
          'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
        ),
      ).filter((element) => element.getClientRects().length > 0);

      if (focusable.length === 0) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = previousOverflow;
    };
  }, [onClose]);

  useEffect(() => {
    setCopied(null);
  }, [rule.id]);

  async function copyText(text: string, target: "id" | "source") {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(target);
    } catch {
      setCopied(null);
    }
  }

  return (
    <div className="fixed inset-0 z-50">
      <div
        aria-hidden="true"
        onClick={onClose}
        className="drawer-backdrop absolute inset-0 bg-black/65"
      />

      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="rule-drawer-title"
        style={{ boxShadow: "-24px 0 60px rgba(0,0,0,0.55)" }}
        className="drawer-panel absolute inset-y-0 right-0 flex w-full max-w-[560px] flex-col border-l border-line-strong bg-surface"
      >
        <header className="flex items-start justify-between gap-4 border-b border-line px-6 py-5">
          <div className="min-w-0">
            <p className="text-[9px] tracking-[0.2em] text-faint">RULE</p>
            <h2
              id="rule-drawer-title"
              className="mt-1 font-mono text-[15px] tracking-tight text-ink"
            >
              {rule.id}
            </h2>
            <p className="mt-1 truncate text-[11px] text-faint">
              {rule.doc_title || rule.doc_id}
            </p>
          </div>
          <div className="flex shrink-0 items-center gap-4">
            <button
              type="button"
              onClick={() => copyText(rule.id, "id")}
              className="text-[11px] text-faint transition-colors hover:text-ink"
            >
              {copied === "id" ? "已复制" : "复制 ID"}
            </button>
            <button
              ref={closeRef}
              type="button"
              onClick={onClose}
              aria-label="关闭详情"
              className="text-faint transition-colors hover:text-ink"
            >
              <CloseGlyph />
            </button>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto">
          <blockquote className="border-l border-accent/60 px-6 py-7">
            <p className="font-serif text-[17px] leading-[1.72] text-ink">
              {rule.rule}
            </p>
          </blockquote>

          <dl className="grid grid-cols-2 gap-x-6 gap-y-5 border-y border-line px-6 py-5 sm:grid-cols-4">
            <div className="min-w-0">
              <dt className="text-[9px] tracking-[0.12em] text-faint">等级</dt>
              <dd
                className={`mt-1.5 font-mono text-[11px] tracking-[0.06em] ${
                  LEVEL_TEXT[rule.enforcement]
                }`}
              >
                {rule.enforcement.toUpperCase()}
              </dd>
            </div>
            <Field label="优先级" value={`P${rule.priority}`} mono />
            <Field label="可覆盖" value={rule.overridable ? "是" : "否"} />
            <Field label="版本" value={`v${rule.version}`} mono />
          </dl>

          <section className="border-b border-line px-6 py-5">
            <h3 className="text-[9px] tracking-[0.16em] text-faint">规则域</h3>
            <p className="mt-2 font-mono text-[11px] text-dim">{rule.domain}</p>
          </section>

          <section className="border-b border-line px-6 py-5">
            <div className="flex items-baseline justify-between gap-4">
              <h3 className="text-[9px] tracking-[0.16em] text-faint">机器检查</h3>
              <span className="font-mono text-[10px] text-faint">
                {rule.check ? rule.check.type : "未配置"}
              </span>
            </div>

            {rule.check ? (
              <dl className="mt-4 space-y-4">
                <Field label="目标" value={rule.check.target} mono />
                <Field label="断言" value={rule.check.assertion} />
                {rule.check.mode ? (
                  <Field label="模式" value={rule.check.mode} mono />
                ) : null}
                {rule.check.pattern ? (
                  <Field label="模式串" value={rule.check.pattern} mono />
                ) : null}
                {rule.check.exclude && rule.check.exclude.length > 0 ? (
                  <Field label="排除" value={rule.check.exclude.join(", ")} mono />
                ) : null}
              </dl>
            ) : (
              <p className="mt-3 max-w-[46ch] text-[11px] leading-relaxed text-faint">
                该规则目前只有自然语言描述，尚无机器断言。断言的执行对象是产品仓，
                待 MVP 脚手架建立后接入扫描器。
              </p>
            )}
          </section>

          <section className="px-6 py-5">
            <h3 className="text-[9px] tracking-[0.16em] text-faint">来源</h3>
            <div className="mt-2 flex items-start justify-between gap-4">
              <p className="min-w-0 break-words font-mono text-[11px] leading-relaxed text-dim">
                {rule.source}
              </p>
              <button
                type="button"
                onClick={() => copyText(rule.source, "source")}
                className="shrink-0 text-[10px] text-faint transition-colors hover:text-ink"
              >
                {copied === "source" ? "已复制" : "复制路径"}
              </button>
            </div>
            <p className="mt-1 font-mono text-[10px] text-faint">
              {rule.doc_id}@v{rule.version}
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
