from __future__ import annotations

from pathlib import Path


SRC_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "stochconn"
if SRC_PACKAGE.is_dir():
    __path__.append(str(SRC_PACKAGE))  # type: ignore[name-defined]

__version__ = "0.2.0"
