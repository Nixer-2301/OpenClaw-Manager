export async function call(method: string, args?: Record<string, unknown>): Promise<unknown> {
  const path = method.startsWith("/") ? method : `/api/${method}`;
  const body = JSON.stringify({ args: args || {}, method });
  const r = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}
