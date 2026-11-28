import "../styles/sections.css";

// end_year is null while a course is still ongoing, so show "Present" instead
function formatYears(startYear, endYear) {
  return endYear ? `${startYear} – ${endYear}` : `${startYear} – Present`;
}

function EducationSection({ education }) {
  // Hide the whole section until real education records exist
  if (!education || education.length === 0) {
    return null;
  }

  // Sort by the display_order set in the admin panel
  const sorted = [...education].sort((a, b) => a.display_order - b.display_order);

  return (
    <section id="education" className="glass-panel portfolio-section">
      <h2 className="section-title">Education</h2>

      <ol className="timeline">
        {sorted.map((item) => (
          <li key={item.id} className="timeline-item">
            <div className="timeline-header">
              <h3 className="timeline-title">
                {item.degree} in {item.field_of_study}
              </h3>
              <span className="timeline-period">
                {formatYears(item.start_year, item.end_year)}
              </span>
            </div>

            <p className="timeline-subtitle">{item.institution}</p>

            {item.grade && <p className="timeline-grade">Grade: {item.grade}</p>}
            {item.description && <p className="timeline-text">{item.description}</p>}
          </li>
        ))}
      </ol>
    </section>
  );
}

export default EducationSection;