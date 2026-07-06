"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { formThesis } from "@/lib/api";

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "8px 10px",
  border: "1px solid #ccced3",
  borderRadius: 6,
  fontSize: 14,
  boxSizing: "border-box",
};

const labelStyle: React.CSSProperties = {
  display: "block",
  fontSize: 13,
  fontWeight: 600,
  margin: "14px 0 4px",
};

export default function NewThesisPage(): React.JSX.Element {
  const router = useRouter();
  const [companyRef, setCompanyRef] = useState("company:acme");
  const [authorRef, setAuthorRef] = useState("author:me");
  const [thesisStatement, setThesisStatement] = useState("");
  const [rationale, setRationale] = useState("");
  const [timeHorizon, setTimeHorizon] = useState("3y");
  const [convictionLevel, setConvictionLevel] = useState(3);
  const [conditions, setConditions] = useState<string[]>([""]);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  function updateCondition(index: number, value: string): void {
    setConditions((prev) => prev.map((c, i) => (i === index ? value : c)));
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();
    setError(null);
    setSubmitting(true);
    const cleaned = conditions.map((c) => c.trim()).filter((c) => c.length > 0);
    const result = await formThesis({
      companyRef,
      authorRef,
      thesisStatement,
      rationale,
      keyAssumptions: [],
      falsificationConditions: cleaned,
      timeHorizon,
      convictionLevel,
    });
    setSubmitting(false);
    if (result.ok) {
      router.push(`/theses/${result.value.id}`);
    } else {
      setError(`${result.error.code}: ${result.error.message}`);
    }
  }

  return (
    <main>
      <a href="/" style={{ fontSize: 13 }}>
        ← Back
      </a>
      <h2 style={{ fontSize: 18 }}>Form a new thesis</h2>
      <form onSubmit={handleSubmit}>
        <label style={labelStyle}>Company reference</label>
        <input
          style={inputStyle}
          value={companyRef}
          onChange={(e) => setCompanyRef(e.target.value)}
          required
        />

        <label style={labelStyle}>Author reference</label>
        <input
          style={inputStyle}
          value={authorRef}
          onChange={(e) => setAuthorRef(e.target.value)}
          required
        />

        <label style={labelStyle}>Thesis statement (the falsifiable claim)</label>
        <textarea
          style={{ ...inputStyle, minHeight: 70 }}
          value={thesisStatement}
          onChange={(e) => setThesisStatement(e.target.value)}
          required
        />

        <label style={labelStyle}>Rationale</label>
        <textarea
          style={{ ...inputStyle, minHeight: 60 }}
          value={rationale}
          onChange={(e) => setRationale(e.target.value)}
        />

        <label style={labelStyle}>
          Falsification conditions (at least one required)
        </label>
        {conditions.map((condition, index) => (
          <input
            key={index}
            style={{ ...inputStyle, marginBottom: 8 }}
            value={condition}
            placeholder="What observable event would prove this wrong?"
            onChange={(e) => updateCondition(index, e.target.value)}
          />
        ))}
        <button
          type="button"
          onClick={() => setConditions((prev) => [...prev, ""])}
          style={{
            fontSize: 13,
            padding: "6px 10px",
            borderRadius: 6,
            border: "1px solid #ccced3",
            background: "white",
            cursor: "pointer",
          }}
        >
          + Add condition
        </button>

        <label style={labelStyle}>Time horizon</label>
        <input
          style={inputStyle}
          value={timeHorizon}
          onChange={(e) => setTimeHorizon(e.target.value)}
          required
        />

        <label style={labelStyle}>Conviction level (1–5)</label>
        <input
          style={inputStyle}
          type="number"
          min={1}
          max={5}
          value={convictionLevel}
          onChange={(e) => setConvictionLevel(Number(e.target.value))}
          required
        />

        {error !== null && (
          <p style={{ color: "#b00020", fontSize: 14 }}>{error}</p>
        )}

        <button
          type="submit"
          disabled={submitting}
          style={{
            marginTop: 18,
            background: "#1a1a1a",
            color: "white",
            padding: "10px 16px",
            borderRadius: 6,
            border: "none",
            fontSize: 14,
            cursor: submitting ? "not-allowed" : "pointer",
          }}
        >
          {submitting ? "Forming…" : "Form thesis"}
        </button>
      </form>
    </main>
  );
}
