"""Seed the Skill Commons with high-fidelity certified skills across 3 domains."""
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from apprentice.models import ContributorSubmission
from apprentice.compiler import SkillCompiler
from apprentice.teach_back import TeachBackEngine
from apprentice.verifier import SkillVerifier
from data.samples.sample_transcripts import SAMPLE_DEMOS

def seed():
    compiler = SkillCompiler()
    engine = TeachBackEngine()
    verifier = SkillVerifier(commons_dir=str(root_dir / "skills_commons"))

    auditors = [
        ("Sarah Jenkins, PE", "LIC-88219", "All electrostatic and optical disk tolerances verified against IEEE standards."),
        ("Elena Rostova, Chief Inspector", "SOLAR-991", "Arc-flash bleed duration and CAT IV multimeter isolation protocol verified."),
        ("Dr. Kevin Thorne", "AGRI-7731", "Soil dielectric calibration and deionized rinsing protocol approved.")
    ]

    for idx, (key, s) in enumerate(SAMPLE_DEMOS.items()):
        print(f"Seeding skill: {s['title']} ({key})...")
        sub = ContributorSubmission(
            contributor_name=s["contributor_name"],
            domain=s["domain"],
            language=s["language"],
            raw_transcript=s["transcript"]
        )
        skill = compiler.compile(sub)
        engine.evaluate_skill(skill)
        
        auditor_name, license_id, notes = auditors[idx]
        ok, msg, sig = verifier.certify_and_publish(skill, auditor_name, license_id, notes)
        print(f"  -> Certified: {ok} | {msg}")

if __name__ == "__main__":
    seed()
