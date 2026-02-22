"""
Eviction Policy — configurable eviction strategies for caches.

Supports LRU, LFU, and FIFO eviction policies with TTL.

Author: Arjun Nair (Performance team)
Last Modified: 2026-03-12
"""

import time
from typing import Any, Dict, List, Optional
from collections import defaultdict


class EvictionPolicy:
    """Base eviction policy with TTL support."""

    def __init__(self, max_size: int, ttl_seconds: int = 300):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.access_count: Dict[str, int] = defaultdict(int)
        self.access_time: Dict[str, float] = {}
        self.insert_time: Dict[str, float] = {}

    def record_access(self, key: str):
        """Record an access to a key, updating frequency and recency."""
        self.access_count[key] += 1
        self.access_time[key] = time.time()
        if key not in self.insert_time:
            self.insert_time[key] = time.time()

    def record_insert(self, key: str):
        """Record a new insertion."""
        self.insert_time[key] = time.time()
        self.access_time[key] = time.time()
        self.access_count[key] = 1

    def get_eviction_candidate_lru(self, keys: List[str]) -> Optional[str]:
        """Get the least recently used key."""
        if not keys:
            return None
        return min(keys, key=lambda k: self.access_time.get(k, 0))

    def get_eviction_candidate_lfu(self, keys: List[str]) -> Optional[str]:
        """Get the least frequently used key."""
        if not keys:
            return None
        return min(keys, key=lambda k: self.access_count.get(k, 0))

    def get_eviction_candidate_fifo(self, keys: List[str]) -> Optional[str]:
        """Get the oldest inserted key (first in, first out)."""
        if not keys:
            return None
        return min(keys, key=lambda k: self.insert_time.get(k, 0))

    def get_expired_keys(self, keys: List[str]) -> List[str]:
        """Get all keys whose TTL has expired."""
        now = time.time()
        expired = []
        for key in keys:
            insert = self.insert_time.get(key, 0)
            if now - insert > self.ttl:
                expired.append(key)
        return expired

    def remove(self, key: str):
        """Clean up tracking data for a removed key."""
        self.access_count.pop(key, None)
        self.access_time.pop(key, None)
        self.insert_time.pop(key, None)

    def reset(self):
        """Reset all tracking data."""
        self.access_count.clear()
        self.access_time.clear()
        self.insert_time.clear()
