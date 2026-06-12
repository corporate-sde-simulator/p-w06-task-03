# Beginner Explanatory Guide: PLATFORM-2935: Fix LRU cache with TTL eviction

> **Task Type**: Product Task  
> **Domain/Focus**: Backend Caching Mechanisms in Python

---

## 1. The Goal (In-Depth Beginner Explanation)

### The Core Problem
The task at hand involves fixing critical bugs in an LRU (Least Recently Used) cache implementation that utilizes TTL (Time To Live) for eviction. Currently, the cache is malfunctioning due to two main issues. The first bug causes the eviction policy to remove the most-recently-used item instead of the least-recently-used item. This is counterintuitive to the purpose of an LRU cache, which is designed to keep the most frequently accessed data while removing the least accessed data when the cache reaches its capacity.

The second bug relates to the TTL mechanism, which is supposed to automatically remove entries that have expired. However, the current implementation incorrectly retains expired entries while evicting fresh ones. This leads to stale data being served to users, which can result in incorrect application behavior and a poor user experience. Fixing these bugs is crucial for maintaining the integrity and performance of the caching system, ensuring that users receive accurate and timely data.

### Jargon Buster (Key Terms Explained)
* **LRU (Least Recently Used)**: This is a caching algorithm that evicts the least recently accessed items first. For example, if you have a cache of size 3 and the items accessed in order are A, B, C, A, then when the next item D is added, item B will be evicted because it was the least recently used.

* **TTL (Time To Live)**: This is a mechanism that defines how long a cache entry should remain valid. For instance, if an entry has a TTL of 300 seconds, it will be removed from the cache after 5 minutes, regardless of how often it is accessed.

* **Eviction Policy**: This refers to the strategy used to determine which items to remove from the cache when it reaches its capacity. Common policies include LRU, LFU (Least Frequently Used), and FIFO (First In, First Out).

* **Cache Thrashing**: This occurs when a cache is constantly evicting and reloading items, leading to poor performance. For example, if the cache size is too small for the workload, it may frequently remove items that are still needed, causing repeated fetches from the slower underlying data store.

### Expected Outcome
After implementing the fixes, the LRU cache should correctly evict the least recently used items when it reaches capacity, ensuring that the most relevant data remains accessible. Additionally, the TTL mechanism should accurately remove expired entries, preventing stale data from being served. 

**Before vs. After**:
- **Before**: The cache may serve stale data and evict frequently accessed items, leading to incorrect application behavior.
- **After**: The cache will serve fresh data and efficiently manage its size by evicting the least recently used items, enhancing performance and user experience.

---

## 2. Related Coding Concepts & Syntax (50% Theory, 50% Practice)

### Concept 1: Caching Mechanisms
#### 📘 Theoretical Overview (50%)
Caching is a technique used to store copies of frequently accessed data in a location that allows for faster retrieval. This is essential in applications where data retrieval from the primary source (like a database) is slow. By keeping a cache, applications can significantly reduce latency and improve performance. If caching is not implemented correctly, it can lead to issues like stale data or excessive memory usage.

The core mechanisms of caching involve:
- **Storage**: Where the cached data is kept (e.g., in-memory, disk).
- **Eviction**: The strategy used to remove old or less relevant data when the cache is full.
- **TTL**: A time-based mechanism that automatically removes data after a specified duration.

#### 💻 Syntax & Practical Examples (50%)
* **Language Syntax**:
  ```python
  class Cache:
      def __init__(self, capacity: int):
          self.capacity = capacity
          self.store = {}

      def get(self, key):
          return self.store.get(key, None)

      def put(self, key, value):
          if len(self.store) >= self.capacity:
              self.evict()
          self.store[key] = value

      def evict(self):
          # Logic to remove an item
          pass
  ```

* **Real-World Application**:
  ```python
  class LRUCache:
      def __init__(self, capacity: int):
          self.capacity = capacity
          self.cache = {}
          self.order = []

      def get(self, key):
          if key in self.cache:
              self.order.remove(key)
              self.order.append(key)
              return self.cache[key]
          return None

      def put(self, key, value):
          if key in self.cache:
              self.order.remove(key)
          elif len(self.cache) >= self.capacity:
              oldest = self.order.pop(0)
              del self.cache[oldest]
          self.cache[key] = value
          self.order.append(key)
  ```

---

## 3. Step-by-Step Logic & Walkthrough

1. **Step 1: Locate and Analyze the Target File**
   * Navigate to the `p-w06-task-03` folder and open `lruCache.py`.
   * Focus on the `put` method and the `_evict_one` method, as these are where the eviction logic is implemented.

2. **Step 2: Input Verification & Validation**
   * Check if the cache is empty or if the key being inserted is `None`. Ensure that the cache size is not exceeded before adding a new entry.

3. **Step 3: Core Implementation / Modification**
   * Modify the `_evict_one` method to ensure it correctly identifies and removes the least recently used item. This can be done by changing the logic that currently evicts the most recently used item.

4. **Step 4: Output Verification & Testing**
   * Run the test suite using `pytest` to ensure that all tests pass. Specifically, check that the cache behaves as expected after the modifications.

---

## 4. Detailed Walkthrough of Test Cases

### Test Case 1: Standard / Success Case
* **Description**: This test checks if the cache correctly retrieves a value that has been stored.
* **Inputs**:
  ```json
  {
      "key": "test_key",
      "value": "test_value"
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The `put` method is called with `key` as "test_key" and `value` as "test_value".
  2. The cache checks if the key already exists; it does not, so it proceeds to add the key-value pair.
  3. The cache size is checked, and since it is below capacity, the item is added successfully.
  4. The `get` method is called with `key` as "test_key".
  5. The cache retrieves the value associated with "test_key" and returns "test_value".
* **Expected Output**: `"test_value"`

### Test Case 2: Edge Case / Validation Fail
* **Description**: This test checks the behavior when trying to retrieve a key that does not exist in the cache.
* **Inputs**:
  ```json
  {
      "key": "non_existent_key"
  }
  ```
* **Step-by-Step Execution Trace**:
  1. The `get` method is called with `key` as "non_existent_key".
  2. The cache checks if the key exists; it does not.
  3. The method increments the miss count in the statistics.
  4. The method returns `None` since the key is not found.
* **Expected Output**: `None`