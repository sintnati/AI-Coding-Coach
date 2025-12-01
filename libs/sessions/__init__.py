# Sessions package
import importlib.util
import sys
from pathlib import Path

# Import session.service.py
spec1 = importlib.util.spec_from_file_location(
    "session_service",
    Path(__file__).parent / "session.service.py"
)
session_service = importlib.util.module_from_spec(spec1)
sys.modules["session_service"] = session_service
spec1.loader.exec_module(session_service)

# Import persistent_session.service.py
spec2 = importlib.util.spec_from_file_location(
    "persistent_session_service",
    Path(__file__).parent / "persistent_session.service.py"
)
persistent_session_service = importlib.util.module_from_spec(spec2)
sys.modules["persistent_session_service"] = persistent_session_service
spec2.loader.exec_module(persistent_session_service)

# Export classes
InMemorySessionService = session_service.InMemorySessionService
PersistentSessionService = persistent_session_service.PersistentSessionService

__all__ = ['InMemorySessionService', 'PersistentSessionService']
