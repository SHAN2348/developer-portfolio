import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/layout/Navbar";
import RevealOnScroll from "../components/common/RevealOnScroll";
import HeroSection from "../sections/HeroSection";
import AboutSection from "../sections/AboutSection";
import ProjectsSection from "../sections/ProjectsSection";
import SkillsSection from "../sections/SkillsSection";
import EducationSection from "../sections/EducationSection";
import ExperienceSection from "../sections/ExperienceSection";
import {
  getPublishedSections,
  findSectionByType,
  getProjects,
  getSkills,
  getEducation,
  getExperience,
} from "../services/portfolioService";

function PortfolioPage() {
  // Read the saved name once, when the page first loads
  const [visitorName] = useState(() => sessionStorage.getItem("visitorName") || "");
  const [sections, setSections] = useState([]);
  const [projects, setProjects] = useState([]);
  const [skills, setSkills] = useState([]);
  const [education, setEducation] = useState([]);
  const [experience, setExperience] = useState([]);
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
        setSections(await getPublishedSections());
      } catch (error) {
        console.error("Could not load portfolio sections:", error);
      }

      try {
        setProjects(await getProjects());
      } catch (error) {
        console.error("Could not load projects:", error);
      }

      try {
        setSkills(await getSkills());
      } catch (error) {
        console.error("Could not load skills:", error);
      }

      try {
        setEducation(await getEducation());
      } catch (error) {
        console.error("Could not load education:", error);
      }

      try {
        setExperience(await getExperience());
      } catch (error) {
        console.error("Could not load experience:", error);
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

        <RevealOnScroll>
          <SkillsSection skills={skills} />
        </RevealOnScroll>

        <RevealOnScroll>
          <EducationSection education={education} />
        </RevealOnScroll>

        <RevealOnScroll>
          <ExperienceSection experiences={experience} />
        </RevealOnScroll>
      </main>
    </div>
  );
}

export default PortfolioPage;