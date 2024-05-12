from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ValidatorResponse:
    is_valid: bool
    data: Optional[Any] = None
    error: Optional[Exception] = None
