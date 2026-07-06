"use client";

import { useEffect, useState } from "react";

import { StatusBadge } from "@/components/StatusBadge";
import { listTheses } from "@/lib/api";
import type { Thesis } from "@/lib/types";

type LoadState =
  | { kind: "loading" }
  | { kind: "error"; message: string }
  | { kind: "loaded"; theses: Thesis[] };

export default function HomePage(): React.JSX.Element {
  const [state, setState] = useState<LoadState>({ kind: "loading" });

  useEffect(() => {
    let active = true;
    void listTheses().then((result) => {
      if (!active) return;
      if (result.ok) {
        setState({ kind: "loaded", theses: result.value.data });
      } else {
        setState({ kind: "error", message: result.error.message });
      }
    });
    return () => {
      active = false;
    };
  }, []);

  return (
    <main>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
        }}
      >
        <h2 style={{ margin: 0, fontSize: 18 }}>Theses</h2>
        <a
          href="/theses/new"
          style={{
            background: "#1a1a1a",
            color: "white",
            padding: "8px 14px",
            borderRadius: 6,
            textDecoration: "none",
            fontSize: 14,
          }}
        >
          + New thesis
        </a>
      </div>

      {state.kind === "loading" && <p>Loading…</p>}
      {state.kind === "error" && (
        <p style={{ color: "#b00020" }}>Error: {state.message}</p>
      )}
      {state.kind === "loaded" && state.theses.length === 0 && (
        <p style={{ color: "#666" }}>
          No theses yet. Form your first — a claim about a company, and what
          would prove it wrong.
        </p>
      )}
      {state.kind === "loaded" &&
        state.theses.map((thesis) => (
          <a
            key={thesis.id}
            href={`/theses/${thesis.id}`}
            style={{
              display: "block",
              background: "white",
              border: "1px solid #e2e4e8",
              borderRadius: 8,
              padding: 14,
              marginBottom: 10,
              textDecoration: "none",
              color: "inherit",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <strong style={{ fontSize: 14 }}>{thesis.companyRef}</strong>
              <StatusBadge status={thesis.status} />
            </div>
            <p style={{ margin: "8px 0 0", fontSize: 14 }}>
              {thesis.thesisStatement}
            </p>
          </a>
        ))}
    </main>
  );
}
