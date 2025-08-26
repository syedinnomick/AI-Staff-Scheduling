import axios from "axios";

class ApiClient {
  constructor(baseURL) {
    this.client = axios.create({
      baseURL: baseURL || "http://127.0.0.1:5000/api",
      headers: { "Content-Type": "application/json" },
    });
  }

  async createStaff(payload) {
    const { data } = await this.client.post("/staff", payload);
    return data;
  }

  async generateSchedule(start_date, days = 7) {
    const { data } = await this.client.post("/generate-schedule", {
      start_date,
      days,
    });
    return data;
  }

  async viewSchedule() {
    const { data } = await this.client.get("/view-schedule");
    return data;
  }
}

const baseURL = import.meta.env.VITE_API_BASE;
const api = new ApiClient(baseURL);
export default api;
