from pydantic import BaseModel, Field, HttpUrl


class ProjectCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=10)
    tech_stack: list[str] = Field(default_factory=list)
    live_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    featured: bool = False

class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=10)
    tech_stack: list[str] | None = None
    live_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    featured: bool | None = None

class ProjectResponse(BaseModel):
    id: str
    title: str
    description: str
    tech_stack: list[str]
    live_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    featured: bool = False


class ProjectListResponse(BaseModel):
    total_projects: int
    page: int
    limit: int
    total_pages: int
    projects: list[ProjectResponse]


class ProjectCreateResponse(BaseModel):
    message: str
    project_id: str
    project: ProjectResponse

class ProjectUpdateResponse(BaseModel):
    message: str
    project_id: str
    updated_fields: dict

class ProjectDeleteResponse(BaseModel):
    message: str
    project_id: str