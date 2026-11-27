import { useEffect, useRef, useState } from "react";
import "../../styles/animations.css";

function RevealOnScroll({ children }) {
  const ref = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // rootMargin "0px 0px -20% 0px" shrinks the bottom of the detection area by 20%.
    // A section only counts as visible once it has moved up into the top 80% of the screen,
    // so sections near the bottom of the first screen don't animate on page load.
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.15, rootMargin: "0px 0px -20% 0px" }
    );

    observer.observe(element);

    return () => observer.disconnect();
  }, []);

  return (
    <div ref={ref} className={`reveal ${isVisible ? "reveal-visible" : ""}`}>
      {children}
    </div>
  );
}

export default RevealOnScroll;