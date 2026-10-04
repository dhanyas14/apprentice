"""Validator for Agent Skills standard (agentskills.io/specification)."""
import re
import yaml
from pathlib import Path
from typing import Tuple, List, Dict, Any

class SkillValidationError(Exception):
    pass

class SkillValidator:
    """Validates skill directory and SKILL.md adherence to the open standard."""
    
    NAME_REGEX = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

    @classmethod
    def validate_content(cls, raw_markdown: str) -> Tuple[bool, List[str], Dict[str, Any]]:
        """Validates raw SKILL.md markdown text."""
        errors = []
        metadata = {}

        if not raw_markdown.strip().startswith("---"):
            errors.append("Skill must start with YAML frontmatter delimiter '---'.")
            return False, errors, metadata

        parts = raw_markdown.split("---", 2)
        if len(parts) < 3:
            errors.append("Invalid YAML frontmatter: closing '---' delimiter not found.")
            return False, errors, metadata

        yaml_content = parts[1]
        body = parts[2]

        try:
            metadata = yaml.safe_load(yaml_content) or {}
        except Exception as e:
            errors.append(f"YAML parsing error in frontmatter: {str(e)}")
            return False, errors, metadata

        # 1. Validate 'name'
        name = metadata.get("name")
        if not name:
            errors.append("Missing required frontmatter field: 'name'.")
        elif not isinstance(name, str):
            errors.append("Field 'name' must be a string.")
        elif not (1 <= len(name) <= 64):
            errors.append("Field 'name' length must be between 1 and 64 characters.")
        elif not cls.NAME_REGEX.match(name):
            errors.append(f"Field 'name' ('{name}') must only contain lowercase alphanumeric characters and single hyphens, no trailing/leading hyphens.")

        # 2. Validate 'description'
        description = metadata.get("description")
        if not description:
            errors.append("Missing required frontmatter field: 'description'.")
        elif not isinstance(description, str):
            errors.append("Field 'description' must be a string.")
        elif len(description) > 1024:
            errors.append("Field 'description' must not exceed 1024 characters.")

        # 3. Validate body structure
        if not body.strip():
            errors.append("Skill body markdown is empty.")
        else:
            required_sections = ["Step", "Safety"]
            for sec in required_sections:
                if sec.lower() not in body.lower():
                    errors.append(f"Recommended procedural section containing '{sec}' not found in markdown body.")

        return len(errors) == 0, errors, metadata

    @classmethod
    def validate_skill_directory(cls, dir_path: str) -> Tuple[bool, List[str]]:
        """Validates an on-disk skill directory."""
        path = Path(dir_path)
        errors = []
        if not path.exists() or not path.is_dir():
            return False, [f"Directory not found: {dir_path}"]

        skill_md = path / "SKILL.md"
        if not skill_md.exists():
            return False, [f"Missing required SKILL.md in {dir_path}"]

        content = skill_md.read_text(encoding="utf-8")
        valid, content_errors, _ = cls.validate_content(content)
        return valid, content_errors
