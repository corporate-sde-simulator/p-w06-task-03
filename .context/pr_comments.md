# PR Review - LRU cache with TTL eviction (by Meera)

## Reviewer: Amit Desai
---

**Overall:** Good foundation but critical bugs need fixing before merge.

### `lruCache.py`

> **Bug #1:** LRU eviction removes most-recently-used item instead of least-recently-used
> This is the higher priority fix. Check the logic carefully and compare against the design doc.

### `evictionPolicy.py`

> **Bug #2:** TTL check uses creation time instead of last access time for sliding TTL
> This is more subtle but will cause issues in production. Make sure to add a test case for this.

---

**Meera**
> Acknowledged. I have documented the issues for whoever picks this up.
