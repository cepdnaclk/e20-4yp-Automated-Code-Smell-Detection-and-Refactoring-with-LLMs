from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SmellRecord(BaseModel):
    type: str
    severity: str = "Moderate"
    location: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)


class RefactorInput(BaseModel):
    file_name: str
    language: str
    smells: List[SmellRecord]
    code: Optional[str] = None


class ValidationStatus(BaseModel):
    syntax: bool = False
    compile: Optional[bool] = None
    structural: Optional[bool] = None
    semantic_check: str = "not_run"
    errors: List[str] = Field(default_factory=list)


class RefactorResult(BaseModel):
    smell_type: str
    strategy: str
    status: str
    rationale: str
    original_code: str
    refactored_code: Optional[str] = None
    validation: ValidationStatus
    metrics: Dict[str, Any] = Field(default_factory=dict)
    category: Optional[str] = None
    group: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[str] = None
    focused_scope: Optional[str] = None
    refactoring_plan: Optional[str] = None


class Summary(BaseModel):
    smells_received: int
    smells_refactored: int
    failures: int


class RefactorOutput(BaseModel):
    file_name: str
    language: str
    results: List[RefactorResult]
    summary: Summary
