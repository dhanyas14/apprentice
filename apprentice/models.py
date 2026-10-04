"""Data models for Apprentice: Agent Skill compiler and verification pipeline."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ContributorSubmission(BaseModel):
    """Input from Person 1 (The Practitioner/Contributor)."""
    contributor_name: str = Field(..., description="Name or handle of contributor")
    domain: str = Field("industrial", description="Domain: electrical, mechanical, solar, agriculture, etc.")
    language: str = Field("en", description="Spoken language of the original demonstration")
    raw_transcript: str = Field(..., description="Spoken or filmed know-how transcript")
    media_url: Optional[str] = Field(None, description="Optional audio or video recording reference")

class TeachBackScenario(BaseModel):
    """An adversarial scenario used to test if the compiled skill works."""
    scenario_id: int
    prompt: str = Field(..., description="Challenging situation or unexpected field condition")
    expected_action: str = Field(..., description="What a safe, knowledgeable practitioner would do")
    student_response: str = Field(..., description="What the agent answered using only the compiled skill")
    score: int = Field(..., ge=0, le=20, description="Score out of 20")
    rubric_feedback: str = Field(..., description="Why the agent scored this, safety compliance notes")

class TeachBackReport(BaseModel):
    """Oral defense / Teach-back evaluation result."""
    total_score: int = Field(..., ge=0, le=100, description="Overall fidelity score (0-100)")
    passed: bool
    scenarios: List[TeachBackScenario]
    summary: str

class LicensedAuditStamp(BaseModel):
    """Verification stamp from Person 2 (The Licensed Auditor)."""
    status: str = Field("pending", description="pending, verified, rejected")
    auditor_name: Optional[str] = None
    license_id: Optional[str] = None
    certifying_authority: Optional[str] = None
    audit_notes: Optional[str] = None
    signature_hash: Optional[str] = None
    timestamp: Optional[str] = None

class CompiledAgentSkill(BaseModel):
    """Standard-compliant Agent Skill object."""
    name: str = Field(..., description="Lowercase hyphenated skill name")
    description: str = Field(..., description="Trigger description for autonomous agents")
    version: str = "1.0.0"
    license: str = "Apache-2.0"
    author: str
    domain: str
    tags: List[str] = []
    triggers: List[str] = []
    prerequisites: List[str] = []
    procedure_steps: List[str] = []
    safety_warnings: List[str] = []
    troubleshooting: Dict[str, str] = {}
    teach_back_report: Optional[TeachBackReport] = None
    verification: LicensedAuditStamp = Field(default_factory=LicensedAuditStamp)
    raw_markdown: Optional[str] = None
