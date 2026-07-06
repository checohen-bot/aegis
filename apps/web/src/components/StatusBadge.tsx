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
  return (
    <span
      style={{
        fontSize: 12,
        fontWeight: 600,
        color: colors[status] ?? "#555",
        textTransform: "uppercase",
      }}
    >
      {status}
    </span>
  );
}
