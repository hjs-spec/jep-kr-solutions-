"""
Korea AI Basic Act Implementation Package
===========================================

This package provides core implementation classes for Korea AI Basic Act compliance.
"""

from .kr_tracker import (
    KoreaAITracker,
    EntityType,
    ContentType,
    LabelingScenario,
    HighImpactSector
)

__version__ = "1.0.0"
__all__ = [
    'KoreaAITracker',
    'EntityType',
    'ContentType',
    'LabelingScenario',
    'HighImpactSector'
]
