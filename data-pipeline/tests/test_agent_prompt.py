from ai.agent import build_system_prompt


def test_agent_prompt_includes_project_skills():
    prompt = build_system_prompt()

    assert "PROJECT SKILLS" in prompt
    assert "salary-analysis" in prompt
    assert "job-search" in prompt
    assert "cover-letter" in prompt
