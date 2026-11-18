---
title: "Implementing a Simple LRU Cache in JavaScript"
description: "Build an array-based JavaScript LRU cache that promotes recently used entries, updates existing keys, and evicts the least recently used item."
author: "sarbull"
tags: [javascript, algorithms]
last_modified_at: 2026-11-18
---

A least recently used (LRU) cache stores a limited number of entries and removes the entry that has gone unused for the longest time when it needs space. This JavaScript example keeps the most recently used entry at the front of an array and the least recently used entry at the end.

## How the cache works

- `get(key)` moves a matching entry to the front and returns its `{ key, value }` object. A missing key returns `-1`.
- `put(key, value)` inserts or updates an entry and marks it as most recently used.
- When an insertion exceeds capacity, `pop()` removes the last entry. Updating an existing key does not evict another entry.
- A capacity of zero keeps the cache empty. Negative or non-integer capacities are rejected.

## Array-based LRU cache implementation

```js
const searchInArrayByObjectKey = (data, key) => {
  return data.find(d => d.key === key);
};

const removeFromArrayByObjectKey = (data, key) => data.filter(d => d.key !== key);

class LRUCache {
  constructor(size) {
    if (!Number.isInteger(size) || size < 0) {
      throw new RangeError("Cache size must be a non-negative integer");
    }

    this.size = size;
    this.cache = []; // Most recently used first; { key, value } entries.
  }

  get(key) {
    const result = searchInArrayByObjectKey(this.cache, key);

    if (!result) {
      return -1;
    }

    this.cache = removeFromArrayByObjectKey(this.cache, key);
    this.cache.unshift(result);
    return result;
  }

  put(key, value) {
    if (this.size === 0) {
      return;
    }

    this.cache = removeFromArrayByObjectKey(this.cache, key);
    this.cache.unshift({ key, value });

    if (this.cache.length > this.size) {
      this.cache.pop();
    }
  }
}
```

The eviction uses [`Array.prototype.pop()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/pop), which removes the final item from the array.

## Example: evict the least recently used entry

```js
const cache = new LRUCache(3);
cache.put(1, 1); // [{key: 1, value: 1}]
cache.put(2, 2); // [{key: 2, value: 2}, {key: 1, value: 1}]
cache.put(3, 3); // [{key: 3, value: 3}, {key: 2, value: 2}, {key: 1, value: 1}]
cache.get(2);    // Returns {key: 2, value: 2}; order is now [2, 3, 1].
cache.put(4, 4); // [{key: 4, value: 4}, {key: 2, value: 2}, {key: 3, value: 3}]
cache.get(1);    // -1: key 1 was the least recently used entry.
cache.put(2, 20); // [{key: 2, value: 20}, {key: 4, value: 4}, {key: 3, value: 3}]
```

## Complexity and limits

This implementation favors a small, readable example. Both `get` and `put` take O(n) time because they search or filter the array; the cache stores O(n) entries. For a cache that needs constant-time lookup and recency updates, use a hash map together with a doubly linked list.

**Correction, 18 November 2026:** the original insertion code stopped accepting new keys when the cache was full. It now inserts the new entry and evicts the least recently used one.
