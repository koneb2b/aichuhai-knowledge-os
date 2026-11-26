import type { Gate } from "@/lib/types";

const GROUP_TITLES: Record<string, string> = {
  G1: "Schema 与域白名单",
  G2: "规则 ID 唯一性",
  G3: "消费端覆盖度",
  G4: "生成物漂移",
  G5: "manifest 清单",
};

function CheckGlyph() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-3 w-3 shrink-0 text-pass"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
    >
      <path d="M3 8.5 6.2 11.7 13 5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function Chevron() {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      className="h-3 w-3 shrink-0 text-faint transition-transform group-open:rotate-90"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
    >
      <path d="m6 4 4 4-4 4" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function GatesPanel({ gates }: { gates: Gate[] }) {
  const groups: string[] = [];
  for (const gate of gates) {
    if (!groups.includes(gate.group)) groups.push(gate.group);
  }
  const passed = gates.filter((gate) => gate.ok).length;

  return (
    <section aria-label="契约闸门">
      <div className="flex items-baseline justify-between">
        <h2 className="text-[10px] tracking-[0.16em] text-faint">契约闸门</h2>
        <span className="font-mono text-[10px] tabular-nums text-dim">
          {passed}
          <span className="text-faint">/{gates.length}</span>
        </span>
      </div>

      <div className="mt-3 border-t border-line">
        {groups.map((group) => {
          const items = gates.filter((gate) => gate.group === group);
          const failed = items.filter((gate) => !gate.ok).length;
          const ok = failed === 0;

          return (
            <details
              key={group}
              open={!ok}
              className="group border-b border-line"
            >
              <summary className="flex cursor-pointer list-none items-center gap-3 py-2.5 [&::-webkit-details-marker]:hidden">
                <span className="font-mono text-[10px] text-faint">{group}</span>
                <span className="min-w-0 flex-1 truncate text-[12px] text-dim group-open:text-ink">
                  {GROUP_TITLES[group] ?? group}
                </span>
                {ok ? (
                  <CheckGlyph />
                ) : (
                  <span className="font-mono text-[10px] text-fail">
                    {failed} 失败
                  </span>
                )}
                <span className="font-mono text-[10px] tabular-nums text-faint">
                  {items.length - failed}/{items.length}
                </span>
                <Chevron />
              </summary>

              <ul className="pb-3 pl-[26px] pr-1">
                {items.map((gate, index) => (
                  <li
                    key={`${group}-${index}`}
                    className="flex gap-2 py-1 text-[11px] leading-snug"
                  >
                    <span
                      aria-hidden="true"
                      className={`mt-[6px] h-1 w-1 shrink-0 ${
                        gate.ok ? "bg-pass/60" : "bg-fail"
                      }`}
                    />
                    <span className="min-w-0">
                      <span className={gate.ok ? "text-dim" : "text-fail"}>
                        {gate.name}
                      </span>
                      {!gate.ok && gate.detail ? (
                        <span className="mt-0.5 block break-words text-[10px] text-faint">
                          {gate.detail}
                        </span>
                      ) : null}
                    </span>
                  </li>
                ))}
              </ul>
            </details>
          );
        })}
      </div>
    </section>
  );
}
