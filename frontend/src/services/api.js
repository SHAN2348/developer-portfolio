import axios from "axios";

// Backend address. Local development uses the FastAPI server on port 8000.
// Replace this with your production backend URL when deploying.
const API_BASE_URL = "http://127.0.0.1:8000/api";

// One shared Axios client used by the whole frontend.
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000, // Stop waiting after 15 seconds
  headers: {
    "Content-Type": "application/json",
  },
});

// Before every request, attach the admin JWT token if one is saved.
// Public requests have no token, so this step is skipped for them.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("adminToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;