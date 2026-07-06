// Small presentational badge for a Thesis lifecycle status. Shared UI primitive,
// kept out of route files so page modules export only a default component.

export function StatusBadge({
  status,
}: {
  status: string;
}): React.JSX.Element {
  const colors: Record<string, string> = {
    draft: "#8a6d3b",
    active: "#2f6f43",
    invalidated: "#b00020",
  };
  const labels: Record<string, string> = {
    draft: "Draft",
    active: "Active",
    invalidated: "Invalidated",
  };
  return (
    <span
      style={{
        fontSize: 12,
        fontWeight: 600,
        color: colors[status] ?? "#555",
      }}
    >
      {labels[status] ?? status}
    </span>
  );
}
