"""Verification protocol for Person 2 (The Licensed Auditor / Certified Inspector)."""
import hashlib
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Tuple
from .models import CompiledAgentSkill, LicensedAuditStamp

# Mock database of certified industry licensing boards
LICENSED_AUTHORITIES = {
    "LIC-88219": {"authority": "National Electrical Contractors & Safety Board", "role": "Senior Safety Engineer"},
    "IRSC-4402": {"authority": "Industrial Robotics & Automation Safety Council", "role": "Principal Automation Auditor"},
    "SOLAR-991": {"authority": "Clean Energy Technical Alliance", "role": "Certified PV Field Inspector"},
    "AGRI-7731": {"authority": "Autonomous Agricultural Systems Registry", "role": "Field Operations Inspector"},
    "MED-3304": {"authority": "Biomedical Equipment Certification Authority", "role": "Clinical Engineering Specialist"}
}

class SkillVerifier:
    """Handles Person 2 credential verification, live interrogation, and cryptographic stamping."""

    def __init__(self, commons_dir: str = "skills_commons"):
        self.commons_dir = Path(commons_dir)
        self.commons_dir.mkdir(parents=True, exist_ok=True)

    def validate_license(self, license_id: str) -> Tuple[bool, str]:
        """Checks if Person 2 holds a recognized company/state certification license."""
        lic = license_id.strip().upper()
        if lic in LICENSED_AUTHORITIES:
            meta = LICENSED_AUTHORITIES[lic]
            return True, f"Verified: {meta['authority']} ({meta['role']})"
        return False, "Unrecognized license ID. Person 2 must hold an authorized company or regulatory license."

    def interrogate_skill(self, skill: CompiledAgentSkill, auditor_question: str) -> str:
        """Allows Person 2 to challenge the AI with an on-the-spot oral question before signing."""
        q = auditor_question.lower()
        # Evaluate knowledge against skill contents
        matched_warnings = [w for w in skill.safety_warnings if any(k in w.lower() for k in q.split())]
        matched_trouble = [f"{k}: {v}" for k, v in skill.troubleshooting.items() if any(t in k.lower() for t in q.split())]

        if matched_warnings:
            return f"[Apprentice AI Response]: Found relevant safety constraint in compiled skill: '{matched_warnings[0]}'. We will enforce complete compliance."
        elif matched_trouble:
            return f"[Apprentice AI Response]: The compiled troubleshooting protocol handles this condition: '{matched_trouble[0]}'."
        else:
            return (
                f"[Apprentice AI Response]: In accordance with '{skill.name}', this condition falls under general precautionary monitoring. "
                f"Prerequisites must remain active: {', '.join(skill.prerequisites[:2])}. If out-of-nominal, abort and notify licensed supervisor."
            )

    def certify_and_publish(self, skill: CompiledAgentSkill, auditor_name: str, license_id: str, audit_notes: str) -> Tuple[bool, str, str]:
        """Certifies the skill, generates cryptographic audit seal, and publishes to Skill Commons."""
        valid, lic_msg = self.validate_license(license_id)
        if not valid:
            return False, lic_msg, ""

        if not skill.teach_back_report or not skill.teach_back_report.passed:
            return False, "Cannot certify: Skill has not passed the Teach-Back fidelity threshold (>=80%).", ""

        timestamp = datetime.utcnow().isoformat() + "Z"
        lic_meta = LICENSED_AUTHORITIES[license_id.strip().upper()]
        certifying_auth = lic_meta["authority"]

        # Generate cryptographic signature hash
        signature_payload = f"{skill.name}:{skill.version}:{license_id}:{skill.teach_back_report.total_score}:{timestamp}"
        signature_hash = hashlib.sha256(signature_payload.encode('utf-8')).hexdigest()

        # Update verification model
        stamp = LicensedAuditStamp(
            status="verified",
            auditor_name=auditor_name,
            license_id=license_id.upper(),
            certifying_authority=certifying_auth,
            audit_notes=audit_notes,
            signature_hash=signature_hash,
            timestamp=timestamp
        )
        skill.verification = stamp

        # Inject verified frontmatter into markdown
        updated_markdown = self._stamp_markdown(skill, stamp)
        skill.raw_markdown = updated_markdown

        # Write to Skill Commons directory
        skill_dir = self.commons_dir / skill.name
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(updated_markdown, encoding="utf-8")

        return True, f"Skill successfully certified by {auditor_name} ({certifying_auth})! Published to {skill_file}", signature_hash

    def _stamp_markdown(self, skill: CompiledAgentSkill, stamp: LicensedAuditStamp) -> str:
        """Updates the YAML frontmatter with the licensed verification seal."""
        frontmatter = {
            "name": skill.name,
            "description": skill.description,
            "version": skill.version,
            "license": skill.license,
            "author": skill.author,
            "domain": skill.domain,
            "tags": skill.tags,
            "fidelity_score": skill.teach_back_report.total_score if skill.teach_back_report else 0,
            "status": "certified",
            "verified_by": f"{stamp.auditor_name} ({stamp.license_id})",
            "certifying_authority": stamp.certifying_authority,
            "audit_timestamp": stamp.timestamp,
            "signature_seal": stamp.signature_hash
        }
        yaml_str = yaml.dump(frontmatter, sort_keys=False).strip()

        # Replace frontmatter
        parts = skill.raw_markdown.split("---", 2)
        body = parts[2] if len(parts) >= 3 else skill.raw_markdown
        return f"---\n{yaml_str}\n---{body}"
