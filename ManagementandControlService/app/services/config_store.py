from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, Optional

from ..models.config_models import Configuration, ConfigurationHistory, ConfigurationVersion

logger = logging.getLogger(__name__)


class ConfigStore:
    """
    Versioned, in-memory configuration store with rollback.

    Note: This is an in-memory placeholder. In production, back with a durable store (e.g., Postgres/TimescaleDB).
    """

    def __init__(self) -> None:
        self._history = ConfigurationHistory()
        self._current: Optional[Configuration] = None
        self._counter = 0

    # PUBLIC_INTERFACE
    def get_current(self) -> Optional[Configuration]:
        """Return the current configuration."""
        return self._current

    # PUBLIC_INTERFACE
    def history(self) -> ConfigurationHistory:
        """Return configuration history and current version reference."""
        return self._history

    # PUBLIC_INTERFACE
    def set_config(self, cfg: Configuration) -> ConfigurationVersion:
        """
        Apply a new configuration and version it.

        Auto-generates a monotonic version string "v<N>" with timestamp metadata.
        """
        self._counter += 1
        version = f"v{self._counter}"
        cv = ConfigurationVersion(version=version, applied_at=datetime.utcnow(), config=cfg)
        self._history.versions.append(cv)
        self._history.current_version = version
        self._current = cfg
        logger.info("Configuration updated to %s", version)
        return cv

    # PUBLIC_INTERFACE
    def rollback(self, version: str) -> ConfigurationVersion:
        """
        Roll back to a previous configuration version by exact version id.

        Raises:
            ValueError: if version unknown.
        """
        target = next((v for v in self._history.versions if v.version == version), None)
        if not target:
            raise ValueError(f"Unknown configuration version: {version}")
        self._current = target.config
        self._history.current_version = target.version
        logger.warning("Configuration rolled back to %s", version)
        return target


# Simple singleton container for DI convenience
_config_store_singleton: Optional[ConfigStore] = None


# PUBLIC_INTERFACE
def get_config_store() -> ConfigStore:
    """FastAPI dependency provider for ConfigStore singleton."""
    global _config_store_singleton
    if _config_store_singleton is None:
        _config_store_singleton = ConfigStore()
    return _config_store_singleton
