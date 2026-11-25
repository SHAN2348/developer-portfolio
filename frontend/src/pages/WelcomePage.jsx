import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "../styles/welcome.css";

const MIN_NAME_LENGTH = 2;
const MAX_NAME_LENGTH = 50;

function WelcomePage() {
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault(); // Stop the browser from reloading the page

    const trimmedName = name.trim(); // Remove spaces at the start and end

    if (trimmedName.length < MIN_NAME_LENGTH) {
      setError(`Please enter at least ${MIN_NAME_LENGTH} characters.`);
      return;
    }
    if (trimmedName.length > MAX_NAME_LENGTH) {
      setError(`Please keep your name under ${MAX_NAME_LENGTH} characters.`);
      return;
    }

    sessionStorage.setItem("visitorName", trimmedName);

    // Record the visit once per browser session, so refreshes don't add extra counts
    if (!sessionStorage.getItem("visitRecorded")) {
      setIsSubmitting(true);
      try {
        await api.post("/visits/", { name: trimmedName });
        sessionStorage.setItem("visitRecorded", "true");
      } catch (requestError) {
        // Don't block the visitor if the backend is unreachable.
        // The portfolio still opens; only the count is missed.
        console.error("Could not record visit:", requestError);
      } finally {
        setIsSubmitting(false);
      }
    }

    navigate("/portfolio");
  }

  return (
    <main className="welcome-page">
      <section className="glass-panel welcome-card">
        <p className="welcome-eyebrow">Welcome to my portfolio</p>
        <h1>Hello there!</h1>
        <p className="welcome-subtitle">Enter your name to continue.</p>

        <form onSubmit={handleSubmit} className="welcome-form">
          <input
            type="text"
            className="welcome-input"
            placeholder="Your name"
            value={name}
            onChange={(event) => {
              setName(event.target.value);
              setError("");
            }}
            autoFocus
            disabled={isSubmitting}
          />
          <button type="submit" className="welcome-button" disabled={isSubmitting}>
            {isSubmitting ? "Please wait..." : "Continue"}
          </button>
        </form>

        {error && <p className="welcome-error">{error}</p>}

        <p className="welcome-subtitle">
          Your name is saved so I know who visited.
        </p>
      </section>
    </main>
  );
}

export default WelcomePage;