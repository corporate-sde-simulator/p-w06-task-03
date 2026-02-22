"""Tests for LRU cache with TTL eviction."""
import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from lruCache import LruCache
from evictionPolicy import EvictionPolicy

class TestMain:
    def test_basic(self):
        obj = LruCache()
        assert obj.process({"key": "val"}) is not None
    def test_empty(self):
        obj = LruCache()
        assert obj.process(None) is None
    def test_stats(self):
        obj = LruCache()
        obj.process({"x": 1})
        assert obj.get_stats()["processed"] == 1

class TestSupport:
    def test_basic(self):
        obj = EvictionPolicy()
        assert obj.process({"key": "val"}) is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
