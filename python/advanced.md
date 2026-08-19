# Python Interview Questions — Advanced

## Q1: Group anagrams together

Given a list of words, group the ones that are anagrams of each other.

**Answer:**
```python
def group_anagrams(words):
    groups = {}
    for word in words:
        sorted_word = "".join(sorted(word))
        if sorted_word not in groups:
            groups[sorted_word] = []
        groups[sorted_word].append(word)
    return list(groups.values())

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

print(group_anagrams([""]))
# [['']]

print(group_anagrams(["abc"]))
# [['abc']]
```
- **Approach:** the sorted-character string is a canonical key shared by all anagrams of the same word — group by that key in a dict. O(n · k log k) time, where k is average word length.

## Q2: Flatten an arbitrarily nested list

Unlike a fixed 2D matrix flatten (see basic.md Q9), this list can be nested to any depth.

**Answer:**
```python
def flatten(lstt):
    result = []
    for item in lstt:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print(flatten([1, [2, 3], [4, [5, 6]], 7]))    # [1, 2, 3, 4, 5, 6, 7]
print(flatten([]))                              # []
print(flatten([1, [2], [[3]], [[[4]]]]))        # [1, 2, 3, 4]
```
- **Approach:** recursion — if an item is itself a list, recurse into it and extend the result; otherwise append directly. O(n) time where n is total element count across all nesting levels. Worth mentioning the iterative alternative (an explicit stack) if asked to avoid recursion depth limits on deeply nested input.

## Q3: Find pairs with a given difference

Given a list and a target difference, return all pairs `(a, b)` from the list where `b - a == target`.

**Answer:**
```python
def pair_difference(nums, target):
    num_set = set(nums)
    seen = set()
    result = []
    for num in nums:
        complement = target + num
        if complement in num_set:
            pairs = (num, complement)
            if pairs not in seen:
                result.append(pairs)
                seen.add(pairs)
    return result

print(pair_difference([1, 5, 3, 4, 2], 2))
# [(1, 3), (3, 5), (2, 4)]
```
- **Approach:** put all values in a set for O(1) lookup, then for each number check whether `num + target` also exists — that pair differs by exactly `target`. A second `seen` set avoids emitting the same pair twice. O(n) time, O(n) space.
