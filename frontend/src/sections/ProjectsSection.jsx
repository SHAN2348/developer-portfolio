import "../styles/sections.css";

function ProjectsSection({ projects }) {
  // Hide the whole section when there are no projects
  if (!projects || projects.length === 0) {
    return null;
  }

  return (
    <section id="projects" className="glass-panel portfolio-section">
      <h2 className="section-title">Projects</h2>

      <div className="projects-grid">
        {projects.map((project) => (
          <article key={project.id} className="project-card">
            <div className="project-card-header">
              <h3 className="project-title">{project.title}</h3>
              {project.featured && <span className="project-featured">Featured</span>}
            </div>

            <p className="project-description">{project.description}</p>

            <ul className="project-tech-list">
              {project.tech_stack.map((tech) => (
                <li key={tech} className="project-tech-tag">
                  {tech}
                </li>
              ))}
            </ul>

            <div className="project-links">
              {project.live_url && (
                <a href={project.live_url} target="_blank" rel="noopener noreferrer">
                  Live demo
                </a>
              )}
              {project.github_url && (
                <a href={project.github_url} target="_blank" rel="noopener noreferrer">
                  GitHub
                </a>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default ProjectsSection;