from datetime import datetime, timezone

from app.db import database


CONTACT_SECTION_TYPE = "contact"


async def get_contact_info(
    is_published: bool | None = True
):
    collection = database.database["portfolio_sections"]

    query = {
        "section_type": CONTACT_SECTION_TYPE
    }

    if is_published is not None:
        query["is_published"] = is_published

    section = await collection.find_one(query)

    if section is None:
        return None

    return section.get("content", {})


async def update_contact_info(contact_data: dict):
    collection = database.database["portfolio_sections"]

    update_fields = {
        f"content.{key}": value
        for key, value in contact_data.items()
    }

    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = await collection.update_one(
        {"section_type": CONTACT_SECTION_TYPE},
        {"$set": update_fields}
    )

    return result.matched_count > 0