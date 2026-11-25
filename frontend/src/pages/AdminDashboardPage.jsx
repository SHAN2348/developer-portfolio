import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "../styles/welcome.css";
import "../styles/admin.css";

function formatDate(isoString) {
  return new Date(isoString).toLocaleString();
}

function AdminDashboardPage() {
  const [summary, setSummary] = useState({ total_visits: 0, unique_visitors: 0 });
  const [visits, setVisits] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    async function loadVisits() {
      try {
        const response = await api.get("/visits/admin");
        setSummary({
          total_visits: response.data.total_visits,
          unique_visitors: response.data.unique_visitors,
        });
        setVisits(response.data.visits);
      } catch (requestError) {
        if (requestError.response?.status === 401) {
          // Token missing or expired: remove it and return to login
          localStorage.removeItem("adminToken");
          navigate("/admin/login");
          return;
        }
        setError("Could not load visit data. Check that the backend is running.");
      } finally {
        setIsLoading(false);
      }
    }

    loadVisits();
  }, [navigate]);

  function handleLogout() {
    localStorage.removeItem("adminToken");
    navigate("/admin/login");
  }

  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <button type="button" className="logout-button" onClick={handleLogout}>
          Log out
        </button>
      </header>

      <section className="dashboard-stats">
        <div className="glass-panel stat-card">
          <p className="stat-label">Total visits</p>
          <p className="stat-value">{summary.total_visits}</p>
        </div>
        <div className="glass-panel stat-card">
          <p className="stat-label">Unique visitors</p>
          <p className="stat-value">{summary.unique_visitors}</p>
        </div>
      </section>

      <section className="glass-panel">
        <h2 style={{ marginBottom: "1rem" }}>Visitors</h2>

        {isLoading && <p className="dashboard-message">Loading visits...</p>}
        {error && <p className="admin-error">{error}</p>}

        {!isLoading && !error && visits.length === 0 && (
          <p className="dashboard-message">No visits recorded yet.</p>
        )}

        {!isLoading && !error && visits.length > 0 && (
          <div className="dashboard-table-wrapper">
            <table className="visits-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Visited at</th>
                </tr>
              </thead>
              <tbody>
                {visits.map((visit) => (
                  <tr key={visit.id}>
                    <td>{visit.name}</td>
                    <td>{formatDate(visit.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  );
}

export default AdminDashboardPage;