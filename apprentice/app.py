"""FastAPI Web Application and REST API for Apprentice."""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .models import ContributorSubmission, CompiledAgentSkill, TeachBackReport
from .compiler import SkillCompiler
from .validator import SkillValidator
from .teach_back import TeachBackEngine
from .verifier import SkillVerifier, LICENSED_AUTHORITIES
from data.samples.sample_transcripts import SAMPLE_DEMOS

app = FastAPI(title="Apprentice", description="Open-Weight Agent Skill Compiler with Teach-Back & Licensed Verification", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# App state storage
STATE: Dict[str, Any] = {
    "current_skill": None,
    "last_submission": None,
    "active_sample_key": "industrial_sensor"
}

compiler = SkillCompiler()
teach_back_engine = TeachBackEngine()
verifier = SkillVerifier(commons_dir=str(Path(__file__).parent.parent / "skills_commons"))

class InterrogateRequest(BaseModel):
    question: str

class CertifyRequest(BaseModel):
    auditor_name: str
    license_id: str
    audit_notes: str

@app.get("/api/samples")
def get_samples():
    return SAMPLE_DEMOS

@app.get("/api/licenses")
def get_licenses():
    return LICENSED_AUTHORITIES

@app.post("/api/compile")
def compile_submission(sub: ContributorSubmission):
    try:
        skill = compiler.compile(sub)
        # Automatically run Teach-Back examination
        report = teach_back_engine.evaluate_skill(skill)
        STATE["current_skill"] = skill
        STATE["last_submission"] = sub
        return {
            "status": "success",
            "skill": skill.dict(),
            "teach_back": report.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/current_skill")
def get_current_skill():
    if not STATE["current_skill"]:
        return {"status": "none"}
    return {
        "status": "active",
        "skill": STATE["current_skill"].dict(),
        "submission": STATE["last_submission"].dict() if STATE["last_submission"] else None
    }

@app.post("/api/interrogate")
def interrogate(req: InterrogateRequest):
    skill = STATE.get("current_skill")
    if not skill:
        raise HTTPException(status_code=400, detail="No active skill compiled yet.")
    answer = verifier.interrogate_skill(skill, req.question)
    return {"answer": answer}

@app.post("/api/certify")
def certify_skill(req: CertifyRequest):
    skill = STATE.get("current_skill")
    if not skill:
        raise HTTPException(status_code=400, detail="No active skill to certify.")
    
    success, msg, sig = verifier.certify_and_publish(
        skill=skill,
        auditor_name=req.auditor_name,
        license_id=req.license_id,
        audit_notes=req.audit_notes
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    
    return {
        "status": "certified",
        "message": msg,
        "signature_hash": sig,
        "skill": skill.dict()
    }

@app.get("/api/commons")
def list_commons():
    commons_path = Path(__file__).parent.parent / "skills_commons"
    skills = []
    if commons_path.exists():
        for d in commons_path.iterdir():
            if d.is_dir() and (d / "SKILL.md").exists():
                content = (d / "SKILL.md").read_text(encoding="utf-8")
                valid, errors, meta = SkillValidator.validate_content(content)
                skills.append({
                    "folder": d.name,
                    "metadata": meta,
                    "valid": valid,
                    "errors": errors,
                    "content": content
                })
    return {"count": len(skills), "skills": skills}

@app.get("/", response_class=HTMLResponse)
def index_html():
    html_file = Path(__file__).parent / "static" / "index.html"
    if html_file.exists():
        return html_file.read_text(encoding="utf-8")
    return "<h1>Apprentice Backend is Running. Static files not yet generated.</h1>"
