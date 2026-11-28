import "../styles/sections.css";

// Group skills by category, keeping the order set by display_order
function groupByCategory(skills) {
  const sorted = [...skills].sort((a, b) => a.display_order - b.display_order);

  return sorted.reduce((groups, skill) => {
    const category = skill.category || "Other";
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(skill);
    return groups;
  }, {});
}

function SkillsSection({ skills }) {
  // Hide the whole section until real skills are added in the admin panel
  if (!skills || skills.length === 0) {
    return null;
  }

  const groups = groupByCategory(skills);

  return (
    <section id="skills" className="glass-panel portfolio-section">
      <h2 className="section-title">Skills</h2>

      <div className="skills-groups">
        {Object.entries(groups).map(([category, items]) => (
          <div key={category} className="skills-group">
            <h3 className="skills-category">{category}</h3>
            <ul className="skills-list">
              {items.map((skill) => (
                <li key={skill.id} className="skill-chip">
                  <span>{skill.name}</span>
                  {skill.proficiency && (
                    <span className="skill-level">{skill.proficiency}</span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}

export default SkillsSection;