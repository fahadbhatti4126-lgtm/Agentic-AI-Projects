from pydantic import BaseModel, Field
from typing import List


class DocumentAnalysis(BaseModel):
    title: str = Field(description="Title of the document")
    summary: str = Field(description="Short summary of the document")
    key_points: List[str] = Field(description="Important points from the document")
    document_type: str = Field(description="Type of document")