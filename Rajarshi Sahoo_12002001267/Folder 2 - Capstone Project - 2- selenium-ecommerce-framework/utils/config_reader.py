"""Configuration loading for the Selenium framework."""

from configparser import ConfigParser
from pathlib import Path


class ConfigReader:
    """Read framework settings from the repository configuration file."""

    def __init__(self) -> None:
        """Load configuration from config/config.ini relative to this module."""
        self.repo_root = Path(__file__).resolve().parent.parent
        self.config_path = self.repo_root / "config" / "config.ini"
        self.parser = ConfigParser()
        self.parser.read(self.config_path)

    def get(self, section: str, key: str) -> str:
        """Return a string setting from the requested section."""
        return self.parser.get(section, key)

    def get_int(self, section: str, key: str) -> int:
        """Return an integer setting from the requested section."""
        return self.parser.getint(section, key)

    def get_bool(self, section: str, key: str) -> bool:
        """Return a boolean setting from the requested section."""
        return self.parser.getboolean(section, key)

    def get_float(self, section, key) -> float:
        """Return a config value as a float."""
        return float(self.parser.get(section, key))


    def get_base_url(self) -> str:
        """Return the configured application base URL."""
        return self.get("app", "base_url")

    @property
    def screenshots_dir(self) -> str:
        """Return the absolute screenshots directory path."""
        return str(self.repo_root / self.get("paths", "screenshots_dir"))

    @property
    def reports_dir(self) -> str:
        """Return the absolute reports directory path."""
        return str(self.repo_root / self.get("paths", "reports_dir"))

    @property
    def test_data_dir(self) -> str:
        """Return the absolute test data directory path."""
        return str(self.repo_root / self.get("paths", "test_data_dir"))


config = ConfigReader()
