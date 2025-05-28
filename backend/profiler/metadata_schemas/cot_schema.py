from pydantic import BaseModel, Field
from typing import Dict, List

class CoTModelSchema(BaseModel):
    reasoning: str = Field(description="Step-by-step thinking process to arrive at the answer.")
    evidence: Dict[str, str] = Field(
        ...,
        description="Mapping from each extracted term to the verbatim quote(s) from the context supporting it.")
    final_answer: List[str] = Field(..., description="Array of up to three distinct terms that directly and specifically answer the field's question, and are also the keys of 'evidence', in the same order.")