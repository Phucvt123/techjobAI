from ai.skills import load_skills, select_skills


def test_load_project_skills():
    skills = load_skills()
    slugs = {skill.slug for skill in skills}

    assert "salary-analysis" in slugs
    assert "job-search" in slugs
    assert "market-insight" in slugs
    assert "cover-letter" in slugs


def test_select_skills_matches_vietnamese_without_accents():
    matched = select_skills("so sanh luong data engineer o HCM")

    assert [skill.slug for skill in matched] == ["salary-analysis"]


def test_select_skills_matches_job_search_intent():
    matched = select_skills("toi muon tim viec remote React phu hop")
    slugs = [skill.slug for skill in matched]

    assert "job-search" in slugs
