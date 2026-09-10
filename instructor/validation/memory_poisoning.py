from __future__ import annotations
import re
from typing import Annotated
from pydantic import AfterValidator

# Common instruction-override patterns associated with OWASP ASI06 memory poisoning
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"disregard previous commands",
    r"system prompt:",
    r"new instructions:",
    r"you are now an unrestricted",
    r"override previous directives",
]

COMPILED_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in INJECTION_PATTERNS]


def validate_no_memory_poisoning(value: str) -> str:
    """
    Validates that a string field does not contain prompt injection payloads
    or memory poisoning overrides (OWASP ASI06). Raises a ValueError
    to trigger Instructor's automatic re-ask cycle if tainted content is detected.
    """
    if not isinstance(value, str):
        return value

    for pattern in COMPILED_PATTERNS:
        if pattern.search(value):
            raise ValueError(
                f"memory_poisoning_detected: Potential prompt injection or memory poisoning detected matching pattern: {pattern.pattern}"
            )
    return value


# Type alias for drop-in usage in Pydantic models
SanitizedStr = Annotated[str, AfterValidator(validate_no_memory_poisoning)]