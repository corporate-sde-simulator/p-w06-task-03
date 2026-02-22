# PLATFORM-2935: Fix LRU cache with TTL eviction

**Status:** In Progress · **Priority:** High
**Sprint:** Sprint 28 · **Story Points:** 5
**Reporter:** Priya Menon (Backend Lead) · **Assignee:** You (Intern)
**Due:** End of sprint (Friday)
**Labels:** `backend`, `python`, `caching`, `performance`
**Task Type:** Bug Fix

---

## Description

Our LRU cache with TTL-based eviction has two critical bugs causing stale data and cache thrashing. The bugs are marked with `# BUG:` comments.

## Acceptance Criteria

- [ ] Bug #1 fixed: Eviction removes most-recently-used item instead of least-recently-used
- [ ] Bug #2 fixed: TTL check uses wrong comparison — keeps expired entries, removes fresh ones
- [ ] All unit tests pass
