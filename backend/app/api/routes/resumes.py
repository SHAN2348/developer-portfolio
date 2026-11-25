from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from app.core.dependencies import get_current_admin
from app.schemas.resume import ResumeCreate, ResumeUpdate
from app.services import resume_service
from app.services.cloudinary_service import upload_certificate_pdf, delete_certificate_pdf

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])


@router.get("/")
async def get_resumes():
    resumes = await resume_service.get_all_resumes()
    return {
        "total_resumes": len(resumes),
        "resumes": resumes
    }


@router.get("/admin")
async def get_all_resumes_for_admin(
    admin_id: str = Depends(get_current_admin)
):
    resumes = await resume_service.get_all_resumes(is_published=None)
    return {
        "total_resumes": len(resumes),
        "resumes": resumes
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_new_resume(
    title: str = Form(default="My Resume"),
    display_order: int = Form(default=10),
    file: UploadFile = File(...),
    admin_id: str = Depends(get_current_admin)
):
    resume_data = ResumeCreate(
        title=title,
        display_order=display_order
    )

    try:
        uploaded_pdf = await upload_certificate_pdf(file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    created_resume = await resume_service.create_resume({
        **resume_data.model_dump(),
        "pdf_url": uploaded_pdf["secure_url"],
        "cloudinary_public_id": uploaded_pdf["public_id"]
    })

    if created_resume is None:
        await delete_certificate_pdf(uploaded_pdf["public_id"])
        raise HTTPException(
            status_code=404,
            detail="Resume section not found. Create it first."
        )

    return {
        "message": "Resume uploaded successfully",
        "resume": created_resume
    }


@router.patch("/{resume_id}")
async def update_existing_resume(
    resume_id: str,
    resume_data: ResumeUpdate,
    admin_id: str = Depends(get_current_admin)
):
    update_data = resume_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update."
        )

    updated = await resume_service.update_resume(resume_id, update_data)

    if not updated:
        raise HTTPException(status_code=404, detail="Resume not found.")

    resume = await resume_service.get_resume_by_id(resume_id)

    return {
        "message": "Resume updated successfully",
        "resume": resume
    }


@router.put("/{resume_id}/pdf")
async def replace_resume_pdf(
    resume_id: str,
    file: UploadFile = File(...),
    admin_id: str = Depends(get_current_admin)
):
    existing_resume = await resume_service.get_resume_by_id(resume_id)

    if existing_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found.")

    try:
        uploaded_pdf = await upload_certificate_pdf(file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    updated = await resume_service.replace_resume_pdf(
        resume_id,
        uploaded_pdf
    )

    if not updated:
        await delete_certificate_pdf(uploaded_pdf["public_id"])
        raise HTTPException(
            status_code=500,
            detail="Failed to update resume PDF."
        )

    old_public_id = existing_resume.get("cloudinary_public_id")

    if old_public_id:
        try:
            await delete_certificate_pdf(old_public_id)
        except Exception:
            pass

    resume = await resume_service.get_resume_by_id(resume_id)

    return {
        "message": "Resume PDF replaced successfully",
        "resume": resume
    }


@router.delete("/{resume_id}")
async def delete_existing_resume(
    resume_id: str,
    admin_id: str = Depends(get_current_admin)
):
    existing_resume = await resume_service.get_resume_by_id(resume_id)

    if existing_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found.")

    deleted = await resume_service.delete_resume(resume_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Resume not found.")

    public_id = existing_resume.get("cloudinary_public_id")

    if public_id:
        try:
            await delete_certificate_pdf(public_id)
        except Exception:
            pass

    return {
        "message": "Resume deleted successfully",
        "resume_id": resume_id
    }