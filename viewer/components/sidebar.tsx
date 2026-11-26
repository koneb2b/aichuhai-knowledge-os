const NAV = [
  { key: "health", label: "契约健康", sub: "Health", version: null },
  { key: "rules", label: "规则浏览器", sub: "Rules", version: null },
  { key: "audit", label: "仓库体检", sub: "Audit", version: "v1" },
  { key: "discovery", label: "选品引擎", sub: "Discovery", version: "v2" },
] as const;

function Wordmark() {
  return (
    <p className="font-mono text-[11px] tracking-[0.22em] text-ink">
      KNOWLEDGE<span className="text-accent">-</span>OS
    </p>
  );
}

export function Sidebar() {
  return (
    <aside className="hidden w-[212px] shrink-0 flex-col border-r border-line bg-base lg:flex">
      <div className="px-6 pb-6 pt-7">
        <Wordmark />
        <p className="mt-2 text-[10px] leading-relaxed text-faint">
          规则契约运行台
          <br />
          本地只读快照
        </p>
      </div>

      <nav aria-label="主导航" className="flex-1 px-4">
        <p className="px-2 pb-2 text-[9px] tracking-[0.18em] text-faint">工作台</p>
        {NAV.filter((item) => item.version === null).map((item, index) => {
          const active = index === 0;
          return (
            <div
              key={item.key}
              aria-current={active ? "page" : undefined}
              className={[
                "flex items-baseline justify-between py-2 pl-2 pr-1",
                active ? "text-ink" : "text-dim",
              ].join(" ")}
            >
              <span className="relative text-[13px]">
                {active ? (
                  <span
                    aria-hidden="true"
                    className="absolute -left-2 top-1/2 h-[14px] w-[2px] -translate-y-1/2 bg-accent"
                  />
                ) : null}
                {item.label}
              </span>
              <span className="font-mono text-[9px] tracking-[0.08em] text-faint">
                {item.sub}
              </span>
            </div>
          );
        })}

        <p className="mt-7 px-2 pb-2 text-[9px] tracking-[0.18em] text-faint">规划</p>
        {NAV.filter((item) => item.version !== null).map((item) => (
          <div
            key={item.key}
            title={`${item.label}：待接入（${item.version}）`}
            className="flex items-baseline justify-between py-2 pl-2 pr-1 text-faint"
          >
            <span className="text-[13px]">{item.label}</span>
            <span className="font-mono text-[9px] tracking-[0.08em]">{item.version}</span>
          </div>
        ))}
      </nav>

      <div className="px-6 py-5">
        <p className="font-mono text-[9px] tracking-[0.14em] text-faint">v0.1 · LOCAL</p>
        <p className="mt-1.5 text-[10px] leading-relaxed text-faint">
          数据来自 compile_rules.py 与 check_rules.py 的产物
        </p>
      </div>
    </aside>
  );
}

export function MobileNav() {
  return (
    <div className="flex items-center justify-between border-b border-line px-5 py-3 lg:hidden">
      <Wordmark />
      <div className="flex items-baseline gap-4 text-[11px]">
        <span className="border-b border-accent pb-0.5 text-ink">契约健康</span>
        <span className="text-faint" title="待接入（v1）">
          体检
        </span>
        <span className="text-faint" title="待接入（v2）">
          选品
        </span>
      </div>
    </div>
  );
}
