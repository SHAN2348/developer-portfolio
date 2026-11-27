import "../styles/sections.css";

function AboutSection({ section }) {
  // Show nothing if the section is missing, unpublished, or has no text
  if (!section || !section.is_published) {
    return null;
  }

  const description = section.content?.description;
  if (!description) {
    return null;
  }

  return (
    <section id="about" className="glass-panel portfolio-section">
      <h2 className="section-title">{section.title}</h2>
      <p className="about-text">{description}</p>
    </section>
  );
}

export default AboutSection;