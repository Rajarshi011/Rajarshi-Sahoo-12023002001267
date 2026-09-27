"""Screenshot capture helpers for failed browser tests."""

import re
from datetime import datetime
from pathlib import Path

from utils.config_reader import config
from utils.logger import log


def capture_screenshot(driver, name: str, folder: str | None = None) -> str | None:
    """Save a timestamped browser screenshot and return its absolute path."""
    try:
        target_folder = Path(folder) if folder else Path(config.screenshots_dir)
        target_folder.mkdir(parents=True, exist_ok=True)
        sanitized_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_") or "screenshot"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = target_folder / f"{sanitized_name}_{timestamp}.png"
        driver.save_screenshot(str(screenshot_path))
        return str(screenshot_path.resolve())
    except Exception as exc:
        log.warning("Could not capture screenshot %s: %s", name, exc)
        return None
