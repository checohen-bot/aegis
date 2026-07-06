"use client";

import { use, useCallback, useEffect, useState } from "react";

import { StatusBadge } from "@/components/StatusBadge";
import {
  activateThesis,
  getThesis,
  invalidateThesis,
} from "@/lib/api";
import type { Thesis } from "@/lib/types";

type LoadState =
  | { kind: "loading" }
  | { kind: "error"; message: string }
  | { kind: "loaded"; thesis: Thesis };

export default function ThesisDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}): React.JSX.Element {
  const { id } = use(params);
  const [state, setState] = useState<LoadState>({ kind: "loading" });
  const [conditionMet, setConditionMet] = useState("");
  const [actionError, setActionError] = useState<string | null>(null);

  const load = useCallback(async (): Promise<void> => {
    const result = await getThesis(id);
    if (result.ok) {
      setState({ kind: "loaded", thesis: result.value });
    } else {
      setState({ kind: "error", message: result.error.message });
    }
  }, [id]);

  useEffect(() => {
    void load();
  }, [load]);

  async function handleActivate(): Promise<void> {
    setActionError(null);
    const result = await activateThesis(id);
    if (result.ok) {
      setState({ kind: "loaded", thesis: result.value });
    } else {
      setActionError(`${result.error.code}: ${result.error.message}`);
    }
  }

  async function handleInvalidate(): Promise<void> {
    setActionError(null);
    const result = await invalidateThesis(id, conditionMet);
    if (result.ok) {
      setState({ kind: "loaded", thesis: result.value });
      setConditionMet("");
    } else {
      setActionError(`${result.error.code}: ${result.error.message}`);
    }
  }

  if (state.kind === "loading") return <p>Loading…</p>;
  if (state.kind === "error")
    return <p style={{ color: "#b00020" }}>Error: {state.message}</p>;

  const thesis = state.thesis;

  return (
    <main>
      <a href="/" style={{ fontSize: 13 }}>
        ← Back
      </a>
      <div
        style={{
          background: "white",
          border: "1px solid #e2e4e8",
          borderRadius: 8,
          padding: 18,
          marginTop: 10,
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <strong>{thesis.companyRef}</strong>
          <StatusBadge status={thesis.status} />
        </div>
        <p style={{ fontSize: 15 }}>{thesis.thesisStatement}</p>

        <Section label="Rationale">{thesis.rationale || "—"}</Section>
        <Section label="Time horizon">{thesis.timeHorizon}</Section>
        <Section label="Conviction level">{`${thesis.convictionLevel} / 5`}</Section>

        <Section label="Falsification conditions">
          <ul style={{ margin: "4px 0", paddingLeft: 18 }}>
            {thesis.falsificationConditions.map((c, i) => (
              <li key={i} style={{ fontSize: 14 }}>
                {c}
              </li>
            ))}
          </ul>
        </Section>

        {thesis.invalidationConditionMet !== null && (
          <Section label="Invalidated because">
            {thesis.invalidationConditionMet}
          </Section>
        )}
      </div>

      {actionError !== null && (
        <p style={{ color: "#b00020", fontSize: 14 }}>{actionError}</p>
      )}

      <div style={{ marginTop: 16 }}>
        {thesis.status === "draft" && (
          <button
            onClick={() => void handleActivate()}
            style={buttonStyle("#2f6f43")}
          >
            Activate
          </button>
        )}
        {thesis.status === "active" && (
          <div>
            <input
              style={{
                width: "100%",
                padding: "8px 10px",
                border: "1px solid #ccced3",
                borderRadius: 6,
                fontSize: 14,
                boxSizing: "border-box",
                marginBottom: 8,
              }}
              placeholder="Which falsification condition was met?"
              value={conditionMet}
              onChange={(e) => setConditionMet(e.target.value)}
            />
            <button
              onClick={() => void handleInvalidate()}
              disabled={conditionMet.trim().length === 0}
              style={buttonStyle("#b00020")}
            >
              Invalidate
            </button>
          </div>
        )}
      </div>
    </main>
  );
}

function Section({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}): React.JSX.Element {
  return (
    <div style={{ marginTop: 12 }}>
      <div style={{ fontSize: 12, fontWeight: 600, color: "#666" }}>
        {label}
      </div>
      <div style={{ fontSize: 14 }}>{children}</div>
    </div>
  );
}

function buttonStyle(bg: string): React.CSSProperties {
  return {
    background: bg,
    color: "white",
    padding: "10px 16px",
    borderRadius: 6,
    border: "none",
    fontSize: 14,
    cursor: "pointer",
  };
}
