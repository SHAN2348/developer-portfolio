import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/layout/Navbar";
import RevealOnScroll from "../components/common/RevealOnScroll";
import HeroSection from "../sections/HeroSection";
import AboutSection from "../sections/AboutSection";
import ProjectsSection from "../sections/ProjectsSection";
import {
  getPublishedSections,
  findSectionByType,
  getProjects,
} from "../services/portfolioService";

function PortfolioPage() {
  // Read the saved name once, when the page first loads
  const [visitorName] = useState(() => sessionStorage.getItem("visitorName") || "");
  const [sections, setSections] = useState([]);
  const [projects, setProjects] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Visitors must enter their name first
    if (!visitorName) {
      navigate("/");
    }
  }, [visitorName, navigate]);

  useEffect(() => {
    async function loadPortfolioData() {
      try {
        const sectionData = await getPublishedSections();
        setSections(sectionData);
      } catch (error) {
        console.error("Could not load portfolio sections:", error);
      }

      try {
        const projectData = await getProjects();
        setProjects(projectData);
      } catch (error) {
        console.error("Could not load projects:", error);
      }
    }

    loadPortfolioData();
  }, []);

  const aboutSection = findSectionByType(sections, "about");

  return (
    <div id="top">
      <Navbar visitorName={visitorName} />
      <main style={{ padding: "0 1.5rem 2rem", maxWidth: "1200px", margin: "0 auto" }}>
        <HeroSection visitorName={visitorName} />

        <RevealOnScroll>
          <AboutSection section={aboutSection} />
        </RevealOnScroll>

        <RevealOnScroll>
          <ProjectsSection projects={projects} />
        </RevealOnScroll>
      </main>
    </div>
  );
}

export default PortfolioPage;