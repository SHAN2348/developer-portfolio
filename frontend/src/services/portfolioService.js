import api from "./api";

// Fetch all published portfolio sections from the public API.
export async function getPublishedSections() {
  const response = await api.get("/portfolio-sections/");
  return response.data.sections;
}

// Find one section by its type, such as "about" or "skills".
export function findSectionByType(sections, sectionType) {
  return sections.find((section) => section.section_type === sectionType) || null;
}

// Fetch the first page of projects from the public API.
// The default page size is 10, which is enough until you have more projects.
export async function getProjects() {
  const response = await api.get("/projects/");
  return response.data.projects;
}