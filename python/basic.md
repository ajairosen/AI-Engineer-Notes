# Python Interview Questions — Basic

## Q1: Palindrome check

Write a function to check if a string is a palindrome, ignoring case and non-alphanumeric characters.

**Answer:**
```python
def is_palindrome(s):
    strr = "".join([i.lower() for i in s if i.isalnum()])
    return strr == strr[::-1]

print(is_palindrome("madam"))                            # True
print(is_palindrome("RaceCar"))                           # True
print(is_palindrome("A man, a plan, a canal: Panama"))    # True
print(is_palindrome("hello"))                              # False
```
- **Approach:** strip non-alphanumeric chars, lowercase, compare to its reverse. O(n) time, O(n) space.

## Q2: Reverse a string

Write a function to reverse a string without using `[::-1]` or `reversed()`.

**Answer:**
```python
def reverse_string(s):
    final_str = ''
    for ch in s:
        final_str = ch + final_str
    return final_str

print(reverse_string("python"))    # "nohtyp"
```
- **Approach:** prepend each character to a growing result string. O(n) time; string concatenation in a loop is O(n²) in the worst case, so mention `''.join(reversed(s))` as the efficient alternative if asked.

## Q3: Count vowels

Write a function that counts the vowels in a string (case-insensitive).

**Answer:**
```python
def count_vowels(s):
    count = 0
    for ch in s:
        if ch.lower() in {'a', 'e', 'i', 'o', 'u'}:
            count += 1
    return count

print(count_vowels('Hello'))    # 2
print(count_vowels('PYTHON'))   # 1
print(count_vowels('aeiou'))    # 5
print(count_vowels('bcdfg'))    # 0
```
- **Approach:** single pass, O(1)-lookup set membership check. O(n) time.

## Q4: Check if two strings are anagrams

Write a function to check whether two strings are anagrams of each other.

**Answer:**
```python
def is_anagram(a, b):
    return "".join(sorted(a)) == "".join(sorted(b))

print(is_anagram("listen", "silent"))    # True
print(is_anagram("hello", "world"))      # False
```
- **Approach:** sort both strings and compare. O(n log n) time; a counting-dict approach gets this to O(n) if asked to optimize.

## Q5: Remove all spaces from a string

**Answer:**
```python
def remove_spaces(words):
    return words.replace(" ", "")

print(remove_spaces("hello world python"))    # "helloworldpython"
```
- **Approach:** built-in `str.replace`, O(n) time.

## Q6: Character frequency count

Write a function that returns a dictionary of character → count for a string.

**Answer:**
```python
def char_frequency(s):
    counter = {}
    for ch in s:
        counter[ch] = counter.get(ch, 0) + 1
    return counter

print(char_frequency("programming"))
# {'p': 1, 'r': 2, 'o': 1, 'g': 2, 'a': 1, 'm': 2, 'i': 1, 'n': 1}
```
- **Approach:** single pass with `dict.get(key, default)` to avoid `KeyError`. O(n) time. `collections.Counter(s)` does the same in one line — worth naming.

## Q7: Reverse each row of a matrix

**Answer:**
```python
def reverse_mat_row(mat):
    return [row[::-1] for row in mat]

print(reverse_mat_row([
    [1, 2, 3],
    [4, 5, 6]
]))
# [[3, 2, 1], [6, 5, 4]]
```
- **Approach:** list comprehension reversing each row independently. O(rows × cols) time.

## Q8: Reverse the row order of a matrix

**Answer:**
```python
def reverse_mat_col(mat):
    return mat[::-1]

print(reverse_mat_col([
    [1, 2, 3],
    [4, 5, 6]
]))
# [[4, 5, 6], [1, 2, 3]]
```
- **Approach:** slicing on the outer list reverses row order (not column order — name is misleading, worth flagging in an interview if given this snippet). O(rows) time.

## Q9: Flatten a 2D matrix

**Answer:**
```python
def flatten_matrix(mat):
    res = []
    for i in mat:
        for j in i:
            res.append(j)
    return res

print(flatten_matrix([
    [1, 2, 3],
    [4, 5, 6]
]))
# [1, 2, 3, 4, 5, 6]
```
- **Approach:** nested loop, works only for exactly 2 levels of nesting. O(rows × cols) time. Contrast with Q2 in [advanced.md](advanced.md), which handles arbitrary nesting via recursion.

## Q10: Print the first N Fibonacci numbers

**Answer:**
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

fibonacci(10)
# 0 1 1 2 3 5 8 13 21 34
```
- **Approach:** iterative with tuple unpacking, O(n) time, O(1) space — no recursion/memoization needed for a plain sequence print.

## Q11: Nth Fibonacci number (recursive)

**Answer:**
```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(4))    # 3
```
- **Approach:** naive recursion, each call branches into two more until it hits the base case. O(2^n) time — exponential, since the same sub-calls (e.g. `fib(2)`) get recomputed many times — O(n) space for the call stack. A `@memoize`/`functools.lru_cache` decorator fixes the recomputation by caching results per argument, bringing it down to O(n).

## Q12: Group words by length

**Answer:**
```python
def group_by_length(words):
    group = {}
    for word in words:
        lenn = len(word)
        if lenn not in group:
            group[lenn] = []
        group[lenn].append(word)
    return group

print(group_by_length(["cat", "dog", "apple", "hi", "bat"]))
# {3: ['cat', 'dog', 'bat'], 5: ['apple'], 2: ['hi']}
```
- **Approach:** dict keyed by length, `setdefault(lenn, []).append(word)` is the one-line equivalent worth mentioning. O(n) time.

## Q13: Intersection of two lists

**Answer:**
```python
def intersection(a, b):
    return list(set(a) & set(b))

print(intersection([1, 2, 2, 3], [2, 2, 4]))    # [2]
print(intersection([1, 2, 3], [4, 5, 6]))       # []
print(intersection([1, 2, 3], [3, 2, 1]))       # [1, 2, 3] (order not guaranteed — set-based)
```
- **Approach:** set intersection. O(n + m) time, but drops duplicates and doesn't preserve input order — mention this tradeoff if order matters.

## Q14: Count duplicate elements

Return a dict of element → count, only for elements that appear more than once.

**Answer:**
```python
def duplicate_counts(nums):
    counter = {}
    for num in nums:
        counter[num] = counter.get(num, 0) + 1
    result = {}
    for num, count in counter.items():
        if count > 1:
            result[num] = count
    return result

print(duplicate_counts([1, 2, 2, 3, 3, 3, 4]))
# {2: 2, 3: 3}
```
- **Approach:** count first, filter second. O(n) time, O(n) space.

## Q15: Remove duplicates while preserving order

**Answer:**
```python
def remove_duplicates(s):
    seen = set()
    result = []
    for ch in s:
        if ch not in seen:
            seen.add(ch)
            result.append(ch)
    return "".join(result)

print(remove_duplicates('programming'))    # "programin"
print(remove_duplicates('aabbcc'))         # "abc"
print(remove_duplicates('hello'))          # "helo"
print(remove_duplicates(''))               # ""
```
- **Approach:** a `set` for O(1) membership checks alongside a list to preserve insertion order — plain `set(s)` would drop the ordering. O(n) time.
