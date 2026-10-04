"""Entrypoint script for Apprentice."""
import sys
import argparse
import uvicorn
from pathlib import Path

# Configure utf-8 encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from apprentice.models import ContributorSubmission
from apprentice.compiler import SkillCompiler
from apprentice.teach_back import TeachBackEngine
from apprentice.verifier import SkillVerifier
from data.samples.sample_transcripts import SAMPLE_DEMOS

def run_cli_demo():
    print("=" * 65)
    print("[*] APPRENTICE: Open-Weight Voice-to-Agent Skill Compiler")
    print("=" * 65)
    
    sample = SAMPLE_DEMOS["industrial_sensor"]
    print(f"\n[1] Ingesting Demo from Person 1: {sample['contributor_name']}")
    print(f"Domain: {sample['domain']} | Language: {sample['language']}")
    print(f"Transcript: {sample['transcript'][:120]}...\n")
    
    compiler = SkillCompiler()
    sub = ContributorSubmission(
        contributor_name=sample["contributor_name"],
        domain=sample["domain"],
        language=sample["language"],
        raw_transcript=sample["transcript"]
    )
    
    print("[2] Compiling to standard Agent Skill (agentskills.io)...")
    skill = compiler.compile(sub)
    print(f"-> Generated skill: {skill.name}")
    print(f"-> Description: {skill.description}")
    
    print("\n[3] Running AI Teach-Back Oral Exam (Adversarial simulation)...")
    engine = TeachBackEngine()
    report = engine.evaluate_skill(skill)
    print(f"-> Teach-Back Fidelity Score: {report.total_score}/100 [PASSED: {report.passed}]")
    for s in report.scenarios[:2]:
        print(f"   Scenario {s.scenario_id}: {s.prompt[:60]}... => Score: {s.score}/20")
        
    print("\n[4] Person 2 (Licensed Auditor Review)...")
    verifier = SkillVerifier(commons_dir=str(root_dir / "skills_commons"))
    auditor_name = "Sarah Jenkins, PE"
    license_id = "LIC-88219"
    notes = "Verified ESD safety and optical zeroing protocols meet industrial standards."
    
    ok, msg, sig = verifier.certify_and_publish(skill, auditor_name, license_id, notes)
    if ok:
        print(f"-> {msg}")
        print(f"-> Cryptographic Audit Seal: {sig}")
        print("\n[5] Skill successfully verified & added to Open Skill Commons!")
    else:
        print(f"-> Certification Failed: {msg}")

def main():
    parser = argparse.ArgumentParser(description="Apprentice: Voice-to-Agent Skill Compiler")
    parser.add_argument("--cli", action="store_true", help="Run end-to-end command-line demonstration")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve web UI")
    args = parser.parse_args()

    if args.cli:
        run_cli_demo()
    else:
        print(f"🚀 Starting Apprentice Web Server at http://{args.host}:{args.port}")
        uvicorn.run("apprentice.app:app", host=args.host, port=args.port, reload=False)

if __name__ == "__main__":
    main()
