"""Offline, synthetic-only delivery control kernel."""

from .contracts import BudgetDisposition, IntentRequest, LifecycleState
from .dispatch import SyntheticDispatchCoordinator

__all__ = [
    "BudgetDisposition",
    "IntentRequest",
    "LifecycleState",
    "SyntheticDispatchCoordinator",
]

__version__ = "0.1.0"