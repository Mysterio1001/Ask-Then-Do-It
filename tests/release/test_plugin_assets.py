import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "adapters" / "codex" / "plugin" / "ask-then-do-it"
ASSETS = PLUGIN / "assets"
CONFIG = ROOT / "release" / "release.json"
BUILDER = ROOT / "scripts" / "build_release.py"


class PluginAssetTests(unittest.TestCase):
    def test_canonical_assets_are_square_transparent_and_nonempty(self) -> None:
        for name, size in (("icon.png", (512, 512)), ("logo.png", (1024, 1024))):
            path = ASSETS / name
            with self.subTest(asset=name):
                self.assertTrue(path.is_file(), f"missing Plugin asset: {path}")
                with Image.open(path) as image:
                    self.assertEqual(image.format, "PNG")
                    self.assertEqual(image.size, size)
                    self.assertIn("A", image.getbands())
                    alpha = image.getchannel("A")
                    self.assertIsNotNone(alpha.getbbox())
                    self.assertEqual(alpha.getpixel((0, 0)), 0)
                    self.assertEqual(alpha.getpixel((image.width - 1, 0)), 0)
                    self.assertEqual(alpha.getpixel((0, image.height - 1)), 0)
                    self.assertEqual(
                        alpha.getpixel((image.width - 1, image.height - 1)), 0
                    )

    def test_manifest_declares_the_approved_interface_assets(self) -> None:
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        interface = manifest["interface"]
        self.assertEqual(interface["brandColor"], "#C8262A")
        self.assertEqual(interface["composerIcon"], "./assets/icon.png")
        self.assertEqual(interface["logo"], "./assets/logo.png")

    def test_codex_builder_copies_assets_without_marketplace_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            output = Path(temporary) / "dist"
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILDER),
                    "--package",
                    "codex",
                    "--allow-test-output-root",
                    "--output-root",
                    str(output),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            package = output / "codex" / "ask-then-do-it"
            self.assertEqual(
                (package / "assets" / "icon.png").read_bytes(),
                (ASSETS / "icon.png").read_bytes(),
            )
            self.assertEqual(
                (package / "assets" / "logo.png").read_bytes(),
                (ASSETS / "logo.png").read_bytes(),
            )
            self.assertFalse(any(package.rglob("marketplace.json")))


if __name__ == "__main__":
    unittest.main()
