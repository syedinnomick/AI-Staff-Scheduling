import React from "react";
import api from "./services/ApiClient";

export default class App extends React.Component {
  state = {
    staff: { name: "", role: "", specialty: "" },
    gen: { start_date: "2025-08-21", days: 7 },
    schedule: [],
    loading: false,
    err: "",
  };

  async componentDidMount() {
    await this.loadSchedule();
  }

  setErr = (msg) => this.setState({ err: msg });
  setLoading = (v) => this.setState({ loading: v });

  loadSchedule = async () => {
    try {
      this.setErr("");
      const data = await api.viewSchedule();
      const schedule = Array.isArray(data) ? data : data?.schedule || [];
      this.setState({ schedule });
    } catch (e) {
      this.setErr(e.message || "Failed to load schedule");
    }
  };

  onAddStaff = async (e) => {
    e.preventDefault();
    const { staff } = this.state;
    if (!staff.name || !staff.role) return this.setErr("Name and role are required");
    try {
      this.setLoading(true); this.setErr("");
      await api.createStaff(staff);
      this.setState({ staff: { name: "", role: "", specialty: "" } });
      // optional: reload schedule if you like
    } catch (e) {
      this.setErr(e.message || "Failed to add staff");
    } finally { this.setLoading(false); }
  };

  onGenerate = async () => {
    const { gen } = this.state;
    try {
      this.setLoading(true); this.setErr("");
      await api.generateSchedule(gen.start_date, Number(gen.days || 7));
      await this.loadSchedule();
    } catch (e) {
      this.setErr(e.message || "Failed to generate schedule");
    } finally { this.setLoading(false); }
  };

  render() {
    const { staff, gen, schedule, loading, err } = this.state;

    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <h1 className="text-2xl font-bold">AI Staff Scheduling — Week 2 Frontend</h1>

        {err && <div className="mt-3 p-3 bg-red-100 text-red-800 rounded">{err}</div>}

        {/* Add Staff */}
        <form onSubmit={this.onAddStaff} className="mt-6 grid grid-cols-1 sm:grid-cols-4 gap-3 bg-white p-4 rounded-xl shadow">
          <input
            className="border rounded px-3 py-2"
            placeholder="Name*"
            value={staff.name}
            onChange={(e) => this.setState({ staff: { ...staff, name: e.target.value } })}
          />
          <input
            className="border rounded px-3 py-2"
            placeholder="Role* (doctor/nurse)"
            value={staff.role}
            onChange={(e) => this.setState({ staff: { ...staff, role: e.target.value } })}
          />
          <input
            className="border rounded px-3 py-2"
            placeholder="Specialty (ICU/ER/...)"
            value={staff.specialty}
            onChange={(e) => this.setState({ staff: { ...staff, specialty: e.target.value } })}
          />
          <button disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50">
            {loading ? "Adding..." : "Add Staff"}
          </button>
        </form>

        {/* Generate Schedule */}
        <div className="mt-6 bg-white p-4 rounded-xl shadow flex flex-col sm:flex-row gap-3 items-start sm:items-end">
          <div>
            <label className="block text-sm text-gray-600">Start date (YYYY-MM-DD)</label>
            <input
              className="border rounded px-3 py-2"
              value={gen.start_date}
              onChange={(e) => this.setState({ gen: { ...gen, start_date: e.target.value } })}
            />
          </div>
          <div>
            <label className="block text-sm text-gray-600">Days</label>
            <input
              type="number"
              min="1"
              max="31"
              className="border rounded px-3 py-2 w-24"
              value={gen.days}
              onChange={(e) => this.setState({ gen: { ...gen, days: e.target.value } })}
            />
          </div>
          <button onClick={this.onGenerate} disabled={loading} className="px-4 py-2 bg-green-600 text-white rounded-lg disabled:opacity-50">
            {loading ? "Generating..." : "Generate Schedule"}
          </button>
        </div>

        {/* Schedule Table */}
        <div className="mt-6 bg-white p-4 rounded-xl shadow overflow-x-auto">
          <h2 className="text-lg font-semibold mb-3">Current Schedule</h2>
          <table className="min-w-full border">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-3 py-2 border">ID</th>
                <th className="px-3 py-2 border">Date</th>
                <th className="px-3 py-2 border">Shift</th>
                <th className="px-3 py-2 border">Staff ID</th>
              </tr>
            </thead>
            <tbody>
              {schedule.map((s) => (
                <tr key={s.id}>
                  <td className="px-3 py-2 border">{s.id}</td>
                  <td className="px-3 py-2 border">{s.date}</td>
                  <td className="px-3 py-2 border">{s.time}</td>
                  <td className="px-3 py-2 border">{s.staff_id ?? "—"}</td>
                </tr>
              ))}
              {schedule.length === 0 && (
                <tr><td className="px-3 py-6 text-center text-gray-500" colSpan={4}>No shifts yet</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}
