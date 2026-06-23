"""Lightweight skill loader for the TechJob AI agent.

Project skills are small markdown playbooks stored in data-pipeline/skills.
They are not executable code. The agent loads them into its system prompt so
recurring workflows (salary analysis, job search, cover letters, market insight)
stay consistent instead of being re-invented on every user message.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SKILLS_DIR = PROJECT_ROOT / "skills"


@dataclass(frozen=True)
class Skill:
    """A markdown skill playbook available to the agent."""

    slug: str
    name: str
    description: str
    triggers: tuple[str, ...]
    content: str


def _extract_heading(content: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", content, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def _extract_field(content: str, field: str) -> str:
    match = re.search(rf"^{field}:\s*(.+)$", content, flags=re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else ""


def _split_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip().lower() for item in value.split(",") if item.strip())


def _normalize(value: str) -> str:
    """Lowercase and remove Vietnamese accents for forgiving trigger matching."""
    decomposed = unicodedata.normalize("NFD", value.lower())
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def load_skills(skills_dir: Path = DEFAULT_SKILLS_DIR) -> list[Skill]:
    """Load every skills/*/SKILL.md file."""
    if not skills_dir.exists():
        return []

    skills: list[Skill] = []
    for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
        content = skill_file.read_text(encoding="utf-8").strip()
        slug = skill_file.parent.name
        skills.append(
            Skill(
                slug=slug,
                name=_extract_heading(content, slug.replace("-", " ").title()),
                description=_extract_field(content, "Description"),
                triggers=_split_csv(_extract_field(content, "Triggers")),
                content=content,
            )
        )
    return skills


def select_skills(message: str, skills: list[Skill] | None = None, max_skills: int = 3) -> list[Skill]:
    """Select skills whose trigger terms appear in the user message."""
    skills = skills if skills is not None else load_skills()
    normalized = _normalize(message)
    matched: list[Skill] = []

    for skill in skills:
        if any(trigger and _normalize(trigger) in normalized for trigger in skill.triggers):
            matched.append(skill)

    return matched[:max_skills]


def render_skill_index(skills: list[Skill] | None = None) -> str:
    """Render a compact list of available skills for the system prompt."""
    skills = skills if skills is not None else load_skills()
    if not skills:
        return "No project skills are currently available."

    lines = []
    for skill in skills:
        trigger_text = ", ".join(skill.triggers) if skill.triggers else "general"
        description = f" — {skill.description}" if skill.description else ""
        lines.append(f"- {skill.name} (`{skill.slug}`){description}. Triggers: {trigger_text}")
    return "\n".join(lines)


def render_full_skills(skills: list[Skill] | None = None) -> str:
    """Render all skill playbooks for injection into the agent prompt."""
    skills = skills if skills is not None else load_skills()
    if not skills:
        return ""

    rendered = []
    for skill in skills:
        rendered.append(f"<skill slug=\"{skill.slug}\">\n{skill.content}\n</skill>")
    return "\n\n".join(rendered)
