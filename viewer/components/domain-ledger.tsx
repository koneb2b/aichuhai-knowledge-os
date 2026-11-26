import type { DomainSummary } from "@/lib/types";

export function DomainLedger({ domains }: { domains: DomainSummary[] }) {
  const total = domains.reduce((sum, domain) => sum + domain.count, 0);
  const max = Math.max(1, ...domains.map((domain) => domain.count));

  return (
    <section aria-label="规则域分布">
      <div className="flex items-baseline justify-between">
        <h2 className="text-[10px] tracking-[0.16em] text-faint">规则域</h2>
        <span className="font-mono text-[10px] tabular-nums text-faint">
          {domains.length} 域 / {total}
        </span>
      </div>

      <div aria-hidden="true" className="mt-3 flex h-[3px] gap-px">
        {domains.map((domain, index) => (
          <span
            key={domain.key}
            style={{
              width: `${(domain.count / Math.max(1, total)) * 100}%`,
              opacity: Math.max(0.28, 1 - index * 0.16),
            }}
            className="bg-accent"
          />
        ))}
      </div>

      <ul className="mt-1">
        {domains.map((domain) => (
          <li
            key={domain.key}
            className="flex items-baseline justify-between gap-4 border-b border-line py-2.5 last:border-b-0"
          >
            <div className="min-w-0">
              <p className="truncate text-[12px] text-dim">{domain.title}</p>
              <p className="mt-0.5 truncate font-mono text-[9px] text-faint">
                {domain.key}
              </p>
            </div>
            <div className="flex shrink-0 items-baseline gap-2">
              <span
                aria-hidden="true"
                style={{ width: `${(domain.count / max) * 22}px` }}
                className="h-[2px] self-center bg-accent/40"
              />
              <span className="font-mono text-[12px] tabular-nums text-ink">
                {domain.count}
              </span>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
