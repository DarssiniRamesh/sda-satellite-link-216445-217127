from __future__ import annotations

import asyncio
import json
import logging
from typing import Set

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WSState:
    """Simple WebSocket connection manager for broadcasting JSON messages."""
    def __init__(self) -> None:
        self._connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._connections.add(ws)

    async def disconnect(self, ws: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(ws)

    async def broadcast_obj(self, obj: object) -> None:
        # Serialize with safe JSON
        data = json.dumps(obj, default=str)
        async with self._lock:
            conns = list(self._connections)
        for ws in conns:
            try:
                await ws.send_text(data)
            except Exception as exc:  # pragma: no cover
                logger.warning("WebSocket send error: %s", exc, exc_info=False)

_ws_singleton: WSState | None = None

# PUBLIC_INTERFACE
def get_ws_state() -> WSState:
    """Dependency provider for global WS manager."""
    global _ws_singleton
    if _ws_singleton is None:
        _ws_singleton = WSState()
    return _ws_singleton
