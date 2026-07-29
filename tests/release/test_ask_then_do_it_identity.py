import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
START_HERE = ROOT / "START-HERE.zh-TW.md"
LICENSE = ROOT / "LICENSE"
THIRD_PARTY_NOTICES = ROOT / "THIRD_PARTY_NOTICES.md"
DESIGN = ROOT / "docs" / "design" / "ai-development-skills.zh-TW.md"

ATTRIBUTION = (
    "This project is an independent extension inspired by Matt Pocock’s skills "
    "repository, particularly grill-me, grilling, and its engineering workflow "
    "skills. Matt Pocock’s original work is licensed under the MIT License. "
    "This project is not affiliated with or endorsed by Matt Pocock."
)

MIT_PERMISSION = (
    "Permission is hereby granted, free of charge, to any person obtaining a copy"
)
MIT_WARRANTY = "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND"


class AskThenDoItIdentityTests(unittest.TestCase):
    def test_root_uses_the_approved_product_identity(self) -> None:
        readme = README.read_text(encoding="utf-8")
        start_here = START_HERE.read_text(encoding="utf-8")

        self.assertTrue(readme.startswith("# Ask Then Do It"))
        self.assertIn("Ask Then Do It", start_here)
        self.assertIn("先問清楚，再開始做", start_here)

    def test_human_design_explanation_uses_current_identity_and_artifacts(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")

        self.assertIn("Ask Then Do It", design)
        self.assertIn("ask-then-do-it-1.0.0.md", design)
        self.assertIn("$ask-with-docs", design)

    def test_readme_places_verbatim_attribution_before_quick_start(self) -> None:
        readme = README.read_text(encoding="utf-8")

        self.assertIn(ATTRIBUTION, readme)
        self.assertIn("https://github.com/mattpocock/skills", readme)
        self.assertIn(
            "https://github.com/mattpocock/skills/blob/main/LICENSE", readme
        )
        self.assertLess(readme.index(ATTRIBUTION), readme.index("START-HERE.zh-TW.md"))

    def test_own_project_mit_license_is_canonical_and_complete(self) -> None:
        self.assertTrue(LICENSE.is_file())
        license_text = LICENSE.read_text(encoding="utf-8")

        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Ian Wu, Handle by me Tech Studio", license_text)
        self.assertIn(MIT_PERMISSION, license_text)
        self.assertIn(MIT_WARRANTY, license_text)

    def test_third_party_notice_preserves_attribution_and_upstream_mit(self) -> None:
        self.assertTrue(THIRD_PARTY_NOTICES.is_file())
        notice = THIRD_PARTY_NOTICES.read_text(encoding="utf-8")

        self.assertIn(ATTRIBUTION, notice)
        self.assertIn("https://github.com/mattpocock/skills", notice)
        self.assertIn(
            "https://github.com/mattpocock/skills/blob/main/LICENSE", notice
        )
        self.assertIn("Copyright (c) 2026 Matt Pocock", notice)
        self.assertIn(MIT_PERMISSION, notice)
        self.assertIn(MIT_WARRANTY, notice)


if __name__ == "__main__":
    unittest.main()
