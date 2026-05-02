"""TDD — i18n helper 동작 검증."""

from core.i18n import apply_i18n, i18n


class TestI18nScalar:
    def test_extracts_ko_when_lang_ko(self):
        assert i18n({"ko": "안녕", "en": "hello"}, "ko") == "안녕"

    def test_extracts_en_when_lang_en(self):
        assert i18n({"ko": "안녕", "en": "hello"}, "en") == "hello"

    def test_falls_back_to_ko_when_en_missing(self):
        assert i18n({"ko": "안녕"}, "en") == "안녕"

    def test_passes_through_scalar(self):
        assert i18n("plain string", "ko") == "plain string"
        assert i18n(42, "ko") == 42

    def test_passes_through_list(self):
        assert i18n(["a", "b"], "ko") == ["a", "b"]

    def test_passes_through_non_i18n_dict(self):
        # Other keys present → not an i18n object → pass through
        assert i18n({"foo": 1, "bar": 2}, "ko") == {"foo": 1, "bar": 2}


class TestApplyI18nRecursion:
    def test_unwraps_nested_i18n_dicts(self):
        obj = {
            "title": {"ko": "제목", "en": "title"},
            "stack": ["Python", "FastAPI"],
            "nested": {
                "summary": {"ko": "요약", "en": "summary"},
                "year": 2026,
            },
        }
        result = apply_i18n(obj, "ko")
        assert result == {
            "title": "제목",
            "stack": ["Python", "FastAPI"],
            "nested": {"summary": "요약", "year": 2026},
        }

    def test_recurses_into_lists(self):
        obj = {
            "items": [
                {"title": {"ko": "1", "en": "1"}},
                {"title": {"ko": "2", "en": "2"}},
            ]
        }
        assert apply_i18n(obj, "en") == {"items": [{"title": "1"}, {"title": "2"}]}

    def test_lang_en_extracts_english(self):
        obj = {"label": {"ko": "한글", "en": "English"}}
        assert apply_i18n(obj, "en") == {"label": "English"}

    def test_partial_translation_fallback(self):
        # en 누락 → ko로 fallback (ADR-02 §2.4)
        obj = {"label": {"ko": "한글만"}}
        assert apply_i18n(obj, "en") == {"label": "한글만"}
