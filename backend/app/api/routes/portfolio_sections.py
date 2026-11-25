from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_admin

from app.schemas.portfolio_section import (
    PortfolioSectionCreate,
    PortfolioSectionUpdate,
    PortfolioSectionResponse
)

from app.services import portfolio_section_service

router = APIRouter(
    prefix="/api/portfolio-sections",
    tags=["Portfolio Sections"]
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_portfolio_section(
    section: PortfolioSectionCreate,
    admin_id: str = Depends(get_current_admin)
):
    section_data = section.model_dump()

    section_id = await portfolio_section_service.create_section(
        section_data
    )

    return {
        "message": "Portfolio section created successfully",
        "section_id": section_id
    }

@router.get("/")
async def get_published_sections():
    sections = await portfolio_section_service.get_all_sections(
        is_published=True
    )

    return {
        "total_sections": len(sections),
        "sections": sections
    }

@router.get("/admin")
async def get_all_portfolio_sections(
    admin_id: str = Depends(get_current_admin)
):
    sections = await portfolio_section_service.get_all_sections()

    return {
        "total_sections": len(sections),
        "sections": sections
    }

@router.get("/{section_id}")
async def get_portfolio_section(
    section_id: str,
    admin_id: str = Depends(get_current_admin)
):
    section = await portfolio_section_service.get_section_by_id(
        section_id
    )

    if section is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio section not found"
        )

    return section

@router.put("/{section_id}")
async def update_portfolio_section(
    section_id: str,
    section: PortfolioSectionCreate,
    admin_id: str = Depends(get_current_admin)
):
    section_data = section.model_dump()

    updated = await portfolio_section_service.update_section(
        section_id,
        section_data
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio section not found"
        )

    return {
        "message": "Portfolio section updated successfully",
        "section_id": section_id
    }

@router.patch("/{section_id}")
async def patch_portfolio_section(
    section_id: str,
    section: PortfolioSectionUpdate,
    admin_id: str = Depends(get_current_admin)
):
    section_data = section.model_dump(
        exclude_unset=True
    )

    if not section_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided"
        )

    updated = await portfolio_section_service.update_section(
        section_id,
        section_data
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio section not found"
        )

    return {
        "message": "Portfolio section partially updated successfully",
        "section_id": section_id,
        "updated_fields": section_data
    }

@router.delete("/{section_id}")
async def delete_portfolio_section(
    section_id: str,
    admin_id: str = Depends(get_current_admin)
):
    deleted = await portfolio_section_service.delete_section(
        section_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio section not found"
        )

    return {
        "message": "Portfolio section deleted successfully",
        "section_id": section_id
    }