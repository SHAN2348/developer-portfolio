from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
    status
)

from app.core.dependencies import get_current_admin


from app.services import (
    certification_service,
    cloudinary_service
)

from app.schemas.certification import (
    CertificationCreate,
    CertificationUpdate
)


router = APIRouter(
    prefix="/api/certifications",
    tags=["Certifications"]
)



@router.get("/")
async def get_certifications():
    certifications = (
        await certification_service.get_all_certifications()
    )

    public_certifications = [
        {
            "id": item["id"],
            "title": item["title"],
            "issuing_organization": item["issuing_organization"],
            "issue_date": item.get("issue_date"),
            "pdf_url": item["pdf_url"],
            "display_order": item["display_order"]
        }
        for item in certifications
    ]

    return {
        "total_certifications": len(public_certifications),
        "certifications": public_certifications
    }


@router.get("/admin")
async def get_all_certifications_for_admin(
    admin_id: str = Depends(get_current_admin)
):
    certifications = (
        await certification_service.get_all_certifications(
            is_published=None
        )
    )

    return {
        "total_certifications": len(certifications),
        "certifications": certifications
    }


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_new_certification(
    title: str = Form(...),
    issuing_organization: str = Form(...),
    issue_date: str | None = Form(default=None),
    display_order: int = Form(default=0),
    file: UploadFile = File(...),
    admin_id: str = Depends(get_current_admin)
):
    certification_data = CertificationCreate(
        title=title,
        issuing_organization=issuing_organization,
        issue_date=issue_date,
        display_order=display_order
    )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    try:
        uploaded_file = await cloudinary_service.upload_pdf(
            file,
            folder="developer-portfolio/certificates"
        )

        certification_data_dict = certification_data.model_dump()

        certification_data_dict["pdf_url"] = uploaded_file["secure_url"]
        certification_data_dict["cloudinary_public_id"] = uploaded_file["public_id"]

        created_certification = (
            await certification_service.create_certification(
                certification_data_dict
            )
        )

        if created_certification is None:
            await cloudinary_service.delete_pdf(
                uploaded_file["public_id"]
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certifications section not found. Create it first."
            )

        return {
            "message": "Certification uploaded successfully",
            "certification": created_certification
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload certification"
        )

    finally:
        await file.close()


@router.patch("/{certification_id}")
async def update_existing_certification(
    certification_id: str,
    certification_data: CertificationUpdate,
    admin_id: str = Depends(get_current_admin)
):
    update_data = certification_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update."
        )

    updated = await certification_service.update_certification(
        certification_id,
        update_data
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found."
        )

    updated_certification = (
        await certification_service.get_certification_by_id(
            certification_id
        )
    )

    return {
        "message": "Certification updated successfully",
        "certification": updated_certification
    }


@router.put("/{certification_id}/pdf")
async def replace_existing_certification_pdf(
    certification_id: str,
    file: UploadFile = File(...),
    admin_id: str = Depends(get_current_admin)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    existing_certification = (
        await certification_service.get_certification_by_id(
            certification_id
        )
    )

    if existing_certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found."
        )

    uploaded_file = None
    database_updated = False

    try:
        uploaded_file = (
            await cloudinary_service.upload_pdf(
                    file,
                    folder="developer-portfolio/certificates"
                )
        )

        updated = await certification_service.replace_certification_pdf(
            certification_id,
            uploaded_file["secure_url"],
            uploaded_file["public_id"]
        )

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certification could not be updated."
            )
        database_updated = True

        old_public_id = existing_certification.get(
            "cloudinary_public_id"
        )

        if old_public_id:
            try:
                await cloudinary_service.delete_pdf(
                    old_public_id
                )
            except Exception:
                pass

        return {
            "message": "Certification PDF replaced successfully",
            "certification": (
                await certification_service.get_certification_by_id(
                    certification_id
                )
            )
        }

    except HTTPException:
        if uploaded_file and not database_updated:
            await cloudinary_service.delete_pdf(
                uploaded_file["public_id"]
            )
        raise

    except ValueError as error:
        if uploaded_file and not database_updated:
            await cloudinary_service.delete_pdf(
                uploaded_file["public_id"]
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    except Exception:
        if uploaded_file and not database_updated:
            await cloudinary_service.delete_pdf(
                uploaded_file["public_id"]
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to replace certification PDF."
        )

    finally:
        await file.close()



@router.delete("/{certification_id}")
async def delete_existing_certification(
    certification_id: str,
    admin_id: str = Depends(get_current_admin)
):
    existing_certification = (
        await certification_service.get_certification_by_id(
            certification_id
        )
    )

    if existing_certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found."
        )

    deleted = await certification_service.delete_certification(
        certification_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification could not be deleted."
        )

    public_id = existing_certification.get(
        "cloudinary_public_id"
    )

    if public_id:
        try:
            await cloudinary_service.delete_pdf(
                public_id
            )
        except Exception:
            pass

    return {
        "message": "Certification deleted successfully",
        "certification_id": certification_id
    }
