from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import os, time
from typing import Callable, Any
from api_manager import KEY_NAMES

@dataclass
class ProviderDiagnostic:
    provider: str
    configured: bool
    status: str
    latency_ms: float | None
    message: str
    checked_at: str

def _now(): return datetime.now(timezone.utc).isoformat()

def diagnose_provider(name: str, probe: Callable[[], Any] | None = None) -> ProviderDiagnostic:
    configured = bool(os.getenv(name, "").strip())
    if not configured:
        return ProviderDiagnostic(name, False, "not_configured", None, "API key is not configured.", _now())
    if probe is None:
        return ProviderDiagnostic(name, True, "configured", None, "Credential detected; no network probe requested.", _now())
    started=time.perf_counter()
    try:
        probe(); latency=(time.perf_counter()-started)*1000
        return ProviderDiagnostic(name, True, "healthy", round(latency,1), "Probe completed successfully.", _now())
    except Exception as exc:
        latency=(time.perf_counter()-started)*1000
        return ProviderDiagnostic(name, True, "degraded", round(latency,1), str(exc)[:240], _now())

def provider_diagnostics() -> list[dict[str, Any]]:
    records=[asdict(diagnose_provider(name)) for name in KEY_NAMES]
    records.insert(0, asdict(ProviderDiagnostic("YAHOO_FINANCE", True, "available", None, "Primary public market-data fallback.", _now())))
    return records
