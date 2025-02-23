# crud.py
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_paragraphs(db: AsyncSession, release_note_id: int, keyword: str):
    query = text("""
        SELECT section_id, metadata, raw_text,
               to_tsvector('english', raw_text) @@ to_tsquery('english', :keyword) AS relevant
        FROM paragraphs
        WHERE release_note_id = :release_note_id
    """)

    result = await db.execute(query, {"release_note_id": release_note_id, "keyword": keyword})
    rows = result.fetchall()

    paragraphs = [
        {"section_id": row.section_id, "raw_text": row.raw_text, "relevant": row.relevant, "metadata": row.metadata}
        for row in rows
    ]
    return paragraphs
