from ai.cover_letter import detect_cv_language, resolve_cover_letter_language


def test_detects_english_cv_language():
    cv_text = """
    Nguyen Huu Khanh Hung
    Skills & Interests
    Programming: Python, C/C++, SQL, R
    Machine Learning: NumPy, Matplotlib, LangChain, LangGraph, HuggingFace
    Activities
    Volunteer Member, Green Summer Campaign
    Developed a handwriting digit recognition application.
    """

    assert detect_cv_language(cv_text) == "English"
    assert resolve_cover_letter_language(cv_text, "Tiếng Việt") == "English"


def test_detects_vietnamese_cv_language():
    cv_text = """
    Nguyễn Văn A
    Kỹ năng: Python, ReactJS, SQL
    Kinh nghiệm: Đã phát triển hệ thống phân tích dữ liệu tuyển dụng.
    Học vấn: Trường Đại học Khoa học Tự nhiên.
    """

    assert detect_cv_language(cv_text) == "Tiếng Việt"
    assert resolve_cover_letter_language(cv_text, "English") == "Tiếng Việt"
