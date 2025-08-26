const API_BASE = "http://127.0.0.1:5000/api";

export async function createStaff(payload) {
  const r = await fetch(`${API_BASE}/staff`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error("Create staff failed");
  return r.json();
}

export async function generateSchedule(start_date, days) {
  const r = await fetch(`${API_BASE}/generate-schedule`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start_date, days }),
  });
  if (!r.ok) throw new Error("Generate schedule failed");
  return r.json();
}

export async function viewSchedule() {
  const r = await fetch(`${API_BASE}/view-schedule`);
  if (!r.ok) throw new Error("Fetch schedule failed");
  return r.json();
}
