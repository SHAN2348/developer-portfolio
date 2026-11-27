import { useState } from "react";
import "../../styles/navbar.css";

// Section links in the order they appear on the page.
// The id must match the id on each section later (for example <section id="projects">).
const NAV_LINKS = [
  { id: "about", label: "About" },
  { id: "projects", label: "Projects" },
  { id: "skills", label: "Skills" },
  { id: "education", label: "Education" },
  { id: "experience", label: "Experience" },
  { id: "certifications", label: "Certifications" },
  { id: "achievements", label: "Achievements" },
  { id: "resume", label: "Resume" },
  { id: "contact", label: "Contact" },
];

function Navbar({ visitorName }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  function closeMenu() {
    setIsMenuOpen(false);
  }

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <a href="#top" className="navbar-brand" onClick={closeMenu}>
          {visitorName ? `Hi, ${visitorName}` : "Portfolio"}
        </a>

        <button
          type="button"
          className="navbar-toggle"
          aria-label="Toggle navigation menu"
          aria-expanded={isMenuOpen}
          onClick={() => setIsMenuOpen((previous) => !previous)}
        >
          {isMenuOpen ? "Close" : "Menu"}
        </button>

        <nav className={`navbar-links ${isMenuOpen ? "navbar-links-open" : ""}`}>
          {NAV_LINKS.map((link) => (
            <a key={link.id} href={`#${link.id}`} onClick={closeMenu}>
              {link.label}
            </a>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default Navbar;