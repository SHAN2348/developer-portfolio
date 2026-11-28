import "../styles/sections.css";

// Show "Present" for ongoing roles; otherwise show the saved end date.
// Dates are shown exactly as saved, because the backend stores them as plain text.
function formatPeriod(item) {
  if (!item.start_date) return "";
  if (item.currently_working) return `${item.start_date} – Present`;
  return item.end_date ? `${item.start_date} – ${item.end_date}` : item.start_date;
}

function ExperienceSection({ experiences }) {
  // Hide the whole section until real experience records exist
  if (!experiences || experiences.length === 0) {
    return null;
  }

  // Sort by the display_order set in the admin panel
  const sorted = [...experiences].sort((a, b) => a.display_order - b.display_order);

  return (
    <section id="experience" className="glass-panel portfolio-section">
      <h2 className="section-title">Experience</h2>

      <ol className="timeline">
        {sorted.map((item) => (
          <li key={item.id} className="timeline-item">
            <div className="timeline-header">
              <h3 className="timeline-title">{item.job_title}</h3>
              <span className="timeline-period">{formatPeriod(item)}</span>
            </div>

            <p className="timeline-subtitle">
              {item.company}
              {item.employment_type && ` · ${item.employment_type}`}
              {item.location && ` · ${item.location}`}
            </p>

            {item.description && <p className="timeline-text">{item.description}</p>}
          </li>
        ))}
      </ol>
    </section>
  );
}

export default ExperienceSection;