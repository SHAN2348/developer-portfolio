import "../styles/hero.css";

function HeroSection({ visitorName }) {
  return (
    <section id="hero" className="hero">
      <div className="glass-panel hero-card">
        <p className="hero-greeting">
          {visitorName ? `Hello ${visitorName}, welcome to my portfolio` : "Welcome to my portfolio"}
        </p>
        <h1 className="hero-name">Shaik Shan Shareef</h1>
        <p className="hero-role">Full-Stack Developer</p>
        <p className="hero-summary">
          I build responsive web applications, Python backend services, and AI-powered solutions.
        </p>
        <a href="#projects" className="welcome-button hero-cta">
          View my projects
        </a>
      </div>
    </section>
  );
}

export default HeroSection;