interface LedgerStripProps {
  total: number;
  domains: number;
  block: number;
  locked: number;
  checks: number;
  artifacts: number;
}

export function LedgerStrip({
  total,
  domains,
  block,
  locked,
  checks,
  artifacts,
}: LedgerStripProps) {
  const cells = [
    { label: "编译规则", value: total, unit: "条" },
    { label: "规则域", value: domains, unit: "个" },
    { label: "硬约束", value: block, unit: "BLOCK" },
    { label: "不可覆盖", value: locked, unit: "条" },
    { label: "机器断言", value: checks, unit: "条" },
    { label: "受契约守卫", value: artifacts, unit: "个生成物" },
  ];

  return (
    <section
      aria-label="编译概览"
      className="grid grid-cols-2 gap-px border-y border-line bg-line sm:grid-cols-3 xl:grid-cols-6"
    >
      {cells.map((cell) => (
        <div key={cell.label} className="bg-base px-4 py-4 xl:px-5">
          <p className="text-[10px] tracking-[0.1em] text-faint">{cell.label}</p>
          <p className="mt-2 flex items-baseline gap-1.5">
            <span className="font-mono text-[23px] leading-none tabular-nums tracking-tight text-ink">
              {cell.value}
            </span>
            <span className="text-[9px] text-faint">{cell.unit}</span>
          </p>
        </div>
      ))}
    </section>
  );
}
