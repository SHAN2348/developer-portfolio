import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "../styles/welcome.css";
import "../styles/admin.css";

function AdminLoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();

    if (!username.trim() || !password) {
      setError("Please enter both username and password.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const response = await api.post("/auth/login", {
        username: username.trim(),
        password,
      });

      // Save the JWT so the api.js interceptor can send it with protected requests
      localStorage.setItem("adminToken", response.data.access_token);

      navigate("/admin/dashboard");
    } catch (requestError) {
      if (requestError.response?.status === 401) {
        setError("Invalid username or password.");
      } else {
        setError("Could not reach the server. Check that the backend is running.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="admin-login-page">
      <section className="glass-panel admin-login-card">
        <h1>Admin Login</h1>
        <p className="admin-login-subtitle">Sign in to manage your portfolio.</p>

        <form onSubmit={handleSubmit} className="admin-form">
          <div>
            <label className="admin-label" htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              className="welcome-input"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              autoComplete="username"
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="admin-label" htmlFor="password">Password</label>
            <div className="admin-password-row">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                className="welcome-input"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                autoComplete="current-password"
                disabled={isLoading}
              />
              <button
                type="button"
                className="admin-toggle-password"
                onClick={() => setShowPassword((previous) => !previous)}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <button type="submit" className="welcome-button" disabled={isLoading}>
            {isLoading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        {error && <p className="admin-error">{error}</p>}
      </section>
    </main>
  );
}

export default AdminLoginPage;