import api from "./api";

// Fetch all published portfolio sections from the public API.
// The backend already filters out unpublished sections.
export async function getPublishedSections() {
  const response = await api.get("/portfolio-sections/");
  return response.data.sections;
}

// Find one section by its type, such as "about" or "skills".
// Returns null if it isn't in the list.
export function findSectionByType(sections, sectionType) {
  return sections.find((section) => section.section_type === sectionType) || null;
}