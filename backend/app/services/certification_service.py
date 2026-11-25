from datetime import datetime, timezone

from bson import ObjectId

from app.db import database


async def create_certification(certification_data: dict):
    collection = database.database["portfolio_sections"]

    certification_data["id"] = str(ObjectId())

    result = await collection.update_one(
        {"section_type": "certifications"},
        {
            "$push": {
                "content.certifications": certification_data
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    if result.matched_count == 0:
        return None

    return certification_data


async def get_all_certifications(
    is_published: bool | None = True
):
    collection = database.database["portfolio_sections"]

    query = {
        "section_type": "certifications"
    }

    if is_published is not None:
        query["is_published"] = is_published

    section = await collection.find_one(query)

    if section is None:
        return []

    return section.get("content", {}).get("certifications", [])


async def get_certification_by_id(certification_id: str):
    collection = database.database["portfolio_sections"]

    section = await collection.find_one({
        "section_type": "certifications"
    })

    if section is None:
        return None

    certifications = section.get("content", {}).get("certifications", [])

    for certification in certifications:
        if certification.get("id") == certification_id:
            return certification

    return None


async def update_certification(
    certification_id: str,
    certification_data: dict
):
    collection = database.database["portfolio_sections"]

    update_fields = {
        f"content.certifications.$.{key}": value
        for key, value in certification_data.items()
    }

    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = await collection.update_one(
        {
            "section_type": "certifications",
            "content.certifications.id": certification_id
        },
        {
            "$set": update_fields
        }
    )

    return result.matched_count > 0


async def replace_certification_pdf(
    certification_id: str,
    pdf_url: str,
    cloudinary_public_id: str
):
    collection = database.database["portfolio_sections"]

    result = await collection.update_one(
        {
            "section_type": "certifications",
            "content.certifications.id": certification_id
        },
        {
            "$set": {
                "content.certifications.$.pdf_url": pdf_url,
                "content.certifications.$.cloudinary_public_id": (
                    cloudinary_public_id
                ),
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return result.matched_count > 0


async def delete_certification(certification_id: str):
    collection = database.database["portfolio_sections"]

    result = await collection.update_one(
        {
            "section_type": "certifications",
            "content.certifications.id": certification_id
        },
        {
            "$pull": {
                "content.certifications": {
                    "id": certification_id
                }
            },
            "$set": {
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return result.modified_count > 0