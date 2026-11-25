
import cloudinary.uploader
from starlette.concurrency import run_in_threadpool
from app.core import cloudinary_config
from io import BytesIO



MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def upload_certificate_pdf(file):
    file_content = await file.read(MAX_FILE_SIZE + 1)

    if not file_content:
        raise ValueError("The uploaded file is empty.")

    if len(file_content) > MAX_FILE_SIZE:
        raise ValueError("PDF file size must not exceed 10 MB.")

    if not file_content.startswith(b"%PDF-"):
        raise ValueError("Only valid PDF files are allowed.")

    pdf_file = BytesIO(file_content)
    pdf_file.name = file.filename or "certificate.pdf"

    result = await run_in_threadpool(
            cloudinary.uploader.upload,
            pdf_file,
            resource_type="raw",
            folder="developer-portfolio/certificates",
            use_filename=True,
            unique_filename=True,
            overwrite=False
        )

    return {
        "public_id": result["public_id"],
        "secure_url": result["secure_url"],
        "format": result.get("format")
    }

async def delete_certificate_pdf(public_id: str):
    result = await run_in_threadpool(
        cloudinary.uploader.destroy,
        public_id,
        resource_type="raw"
    )

    return result.get("result") == "ok"