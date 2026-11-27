import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/layout/Navbar";
import HeroSection from "../sections/HeroSection";
import AboutSection from "../sections/AboutSection";
import {
  getPublishedSections,
  findSectionByType,
} from "../services/portfolioService";

function PortfolioPage() {
  // Read the saved name once, when the page first loads
  const [visitorName] = useState(() => sessionStorage.getItem("visitorName") || "");
  const [sections, setSections] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Visitors must enter their name first
    if (!visitorName) {
      navigate("/");
    }
  }, [visitorName, navigate]);

  useEffect(() => {
    async function loadSections() {
      try {
        const data = await getPublishedSections();
        setSections(data);
      } catch (error) {
        // If the backend is down, the page still shows the hero and navbar
        console.error("Could not load portfolio sections:", error);
      }
    }

    loadSections();
  }, []);

  const aboutSection = findSectionByType(sections, "about");

  return (
    <div id="top">
      <Navbar visitorName={visitorName} />
      <main style={{ padding: "0 1.5rem 2rem", maxWidth: "1200px", margin: "0 auto" }}>
        <HeroSection visitorName={visitorName} />
        <AboutSection section={aboutSection} />
      </main>
    </div>
  );
}

export default PortfolioPage;