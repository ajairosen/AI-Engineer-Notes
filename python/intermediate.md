# Python Interview Questions — Intermediate

## Q1: Decorator vs. decorator factory

What's the difference between a decorator that takes arguments (e.g., `@retry(times=3)`) and one that doesn't (e.g., `@log_calls`)? Write a simple `@retry(times=3)` decorator.

**Answer:**

*Plain decorator (`@log_calls`)*
- Function takes the target function, returns a wrapped version.
- One level of nesting.

*Decorator factory (`@retry(times=3)`)*
- Function takes the decorator's own args, returns a decorator.
- Two levels of nesting — `retry(times=3)` runs first, its return value wraps the function.

```python
import functools, time

def retry(times=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator
```
- `functools.wraps` preserves original `__name__`/`__doc__` — worth mentioning.

## Q2: First non-repeating character

Return the first character in a string that appears exactly once, or `None` if there isn't one.

**Answer:**
```python
def first_non_repeating(s):
    counter = {}
    for ch in s:
        counter[ch] = counter.get(ch, 0) + 1
    for ch in s:
        if counter[ch] == 1:
            return ch
    return None

print(first_non_repeating('leetcode'))    # 'l'
print(first_non_repeating('aabbcc'))      # None
print(first_non_repeating('aabbccd'))     # 'd'
print(first_non_repeating('swiss'))       # 'w'
```
- **Approach:** two passes — one to build counts, one to find the first count-1 char in original order. O(n) time, O(n) space.

## Q3: Second largest number in a list

**Answer:**
```python
def second_largest(nums):
    largest = None
    second = None
    for num in nums:
        if largest is None or num > largest:
            second = largest
            largest = num
        if num != largest and (second is None or num > second):
            second = num
    return second

print(second_largest([1, 2, 3, 4, 5]))    # 4
print(second_largest([5, 5, 5]))          # None (no distinct second value)
print(second_largest([10]))               # None
print(second_largest([3, 1, 4, 4, 2]))    # 3
print(second_largest([-5, -2, -10]))      # -5
```
- **Approach:** single pass tracking both largest and second-largest, handling ties/duplicates by requiring `num != largest`. O(n) time, O(1) space — avoids sorting (O(n log n)).

## Q4: Most frequent character in a string

**Answer:**
```python
def most_frequent(s):
    counter = {}
    for ch in s:
        counter[ch] = counter.get(ch, 0) + 1
    return max(counter, key=counter.get)

print(most_frequent("aabbcccdd"))    # "c"
```
- **Approach:** build a frequency dict, then `max(dict, key=dict.get)` to pick the highest-count key. O(n) time.

## Q5: Most common element in a list

**Answer:**
```python
def most_common(nums):
    counter = {}
    for num in nums:
        counter[num] = counter.get(num, 0) + 1
    return max(counter, key=counter.get)

print(most_common([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4]))    # 4 (appears 5 times)
```
- **Approach:** same pattern as Q4, generalized to any hashable type. `collections.Counter(nums).most_common(1)` is the standard-library one-liner worth naming.

## Q6: First duplicate element in a list

Return the first element that repeats (by first point of repetition), or `None`.

**Answer:**
```python
def first_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)

print(first_duplicate([2, 1, 3, 5, 3, 2]))    # 3
print(first_duplicate([1, 2, 3, 4]))          # None
print(first_duplicate([2, 2, 1, 1]))          # 2
print(first_duplicate([]))                    # None
```
- **Approach:** single pass with a `set` for O(1) lookups. O(n) time, O(n) space.

## Q7: All duplicate elements in a list

Return every element that occurs more than once, in order of their second occurrence.

**Answer:**
```python
def find_duplicates(nums):
    dups = []
    seen = set()
    for num in nums:
        if num not in seen:
            seen.add(num)
        else:
            dups.append(num)
    return dups

print(find_duplicates([1, 2, 3, 2, 4, 5, 1]))    # [2, 1]
```
- **Approach:** same seen-set pattern as Q6, but collects every repeat rather than returning early. O(n) time.

## Q8: Find the missing number in a sequence

Given a list containing `n-1` distinct numbers from `1` to `n`, find the missing one.

**Answer:**
```python
def missing_number(nums):
    n = len(nums) + 1
    expected = n * (n + 1) // 2
    return expected - sum(nums)

print(missing_number([1, 2, 4, 5, 6]))    # 3
```
- **Approach:** Gauss's sum formula for `1..n` minus the actual sum. O(n) time, O(1) space — avoids sorting or a hash set.

## Q9: Move all zeros to the end

**Answer:**
```python
def move_zeros(nums):
    with_zeros = [i for i in nums if i == 0]
    without_zeros = [i for i in nums if i != 0]
    return without_zeros + with_zeros

print(move_zeros([0, 1, 3, 0, 12]))    # [1, 3, 12, 0, 0]
```
- **Approach:** two list comprehensions, preserves relative order of non-zero elements. O(n) time, O(n) space. An in-place two-pointer swap gets this to O(1) space if asked to optimize.

## Q10: Reverse the order of words in a sentence

**Answer:**
```python
def reverse_words(words):
    result = ""
    for word in words.split(" "):
        result = word + " " + result
    return result

print(reverse_words("hello world python"))
# "python world hello "  (note the trailing space from the concatenation pattern)
```
- **Approach:** split on spaces, prepend each word to build the reversed order. O(n) time. `" ".join(words.split()[::-1])` is the cleaner idiomatic version (and avoids the trailing-space bug) — good to mention.

## Q11: Rotate a list by k positions

**Answer:**
```python
def rotate(nums, k):
    if not nums:
        return nums
    k = k % len(nums)
    return nums[-k:] + nums[:-k]

print(rotate([1, 2, 3, 4, 5], 2))    # [4, 5, 1, 2, 3]
print(rotate([1, 2, 3], 4))          # [3, 1, 2]
print(rotate([], 3))                 # []
```
- **Approach:** `k % len(nums)` handles `k` larger than the list length; slicing does a right-rotation in one line. O(n) time, O(n) space (new list).

## Q12: Transpose a matrix

**Answer:**
```python
def transpose(mat):
    return [list(row) for row in zip(*mat)]

print(transpose([
    [1, 2, 3],
    [4, 5, 6]
]))
# [[1, 4], [2, 5], [3, 6]]

print(transpose([]))
# []
```
- **Approach:** `zip(*mat)` unpacks each row as a separate argument and zips them column-wise. O(rows × cols) time. Worth being able to explain the `*` unpacking clearly, since interviewers often probe it.

## Q13: Two sum

Given a list and a target, return the indices of the two numbers that add up to it.

**Answer:**
```python
def two_sum(nums, target):
    seen = {}
    for idx, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], idx]
        seen[num] = idx
    return []

print(two_sum([2, 7, 11, 15], 9))    # [0, 1]
```
- **Approach:** single pass with a value→index hash map, checking for the complement before inserting the current number. O(n) time, O(n) space — the classic improvement over the O(n²) brute-force pair check.

## Q14: Longest substring without repeating characters

Given a string, find the length of the longest substring without repeating characters.

**Answer:**
```python
def longest_unique_substring(s):
    longest = 0
    l = 0
    seen = set()
    for r in range(len(s)):
        while s[r] in seen:
            seen.remove(s[l])
            l += 1
        w = (r - l) + 1
        longest = max(longest, w)
        seen.add(s[r])
    return longest

print(longest_unique_substring("abcabcbb"))    # 3  ("abc")
print(longest_unique_substring("bbbbb"))       # 1  ("b")
print(longest_unique_substring("pwwkew"))      # 3  ("wke")
print(longest_unique_substring(""))            # 0
print(longest_unique_substring("abcdab"))      # 4  ("cdab")
```
- **Approach:** sliding window with two pointers (`l`, `r`) and a `seen` set. `r` expands the window; whenever `s[r]` is already in the window, shrink from the left (evicting from `seen`, advancing `l`) until the duplicate is gone. O(n) time — each character enters and leaves `seen` at most once — O(k) space where k is the window's character-set size.

## Q15: Check if one string is a rotation of another

**Answer:**
```python
def is_rotation(s1, s2):
    if len(s1) != len(s2):
        return False
    return s2 in (s1 + s1)

print(is_rotation("waterbottle", "erbottlewat"))   # True
print(is_rotation("hello", "llohe"))               # True
print(is_rotation("hello", "helol"))               # False
print(is_rotation("abc", "abcd"))                  # False
```
- **Approach:** concatenating `s1` with itself contains every rotation of `s1` as a substring — check membership after a length guard. O(n) time, O(n) space (for `s1+s1`). A brute-force alternative checks each of the n rotations individually — O(n²) time, more code but no trick to remember.

## Q16: `@memoize` decorator

Write a decorator `@memoize` that caches a function's return value based on its arguments, so repeated calls with the same args skip recomputation. Test it on a recursive Fibonacci function.

**Answer:**
```python
from functools import wraps
import time

def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    wrapper.cache = cache
    return wrapper

@memoize
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

start = time.perf_counter()
print(fib(30))                                    # 832040
print(f"time: {time.perf_counter() - start:.6f}s")

print("cache size:", len(fib.cache))               # 31 (n = 0..30)

start = time.perf_counter()
print(fib(30))                                     # 832040, served from cache
print(f"second call time: {time.perf_counter() - start:.8f}s")
```
- **Approach:** the wrapper builds a key from `(args, sorted kwargs)` and only calls the real function on a cache miss — turns naive exponential recursion (see basic.md Q11) into O(n) by never recomputing a given `n` twice. Space: O(n) for the cache.
- **Common bugs to watch for:** decorate with `@wraps(func)` directly if you did `from functools import wraps` — writing `@functools.wraps(func)` without importing `functools` itself raises `NameError`. Also, even with memoization, don't warm up with something like `fib(1000)`: the *first* call still has to recurse all the way down to the base case before anything is cached, so it hits Python's default recursion limit (1000) and raises `RecursionError` — memoization speeds up repeated calls, it doesn't remove the initial stack depth.

## Q17: Valid (balanced) parentheses

Given a string containing just `(`, `)`, `{`, `}`, `[`, `]`, determine if the brackets are validly matched/balanced.

**Answer:**
```python
def is_balanced(s):
    stack = []
    pairs = {
        "}": "{",
        "]": "[",
        ")": "("
    }
    for ch in s:
        if ch in "{[(":
            stack.append(ch)
        elif ch in "}])":
            if not stack:
                return False
            top = stack.pop()
            if top != pairs[ch]:
                return False
    return len(stack) == 0

print(is_balanced("()"))            # True
print(is_balanced("([{}])"))        # True
print(is_balanced("(]"))            # False
print(is_balanced("([)]"))          # False
print(is_balanced("((("))           # False
print(is_balanced(""))              # True
```
- **Approach:** stack-based matching. Push every opener. On a closer, either the stack is empty (unmatched closer, e.g. leading `)`) or the popped top isn't its expected opener (wrong type or interleaved brackets, e.g. `([)]`) — both return `False` immediately. After the loop, `len(stack) == 0` catches unclosed openers (e.g. `"((("`). O(n) time, O(n) space (worst case: all openers).
