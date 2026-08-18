# Python Interview Questions (Basics → Intermediate)

## Q1: Palindrome check

Write a function to check if a string is a palindrome, ignoring case and non-alphanumeric characters (e.g., `"A man, a plan, a canal: Panama"` → `True`). What's the time/space complexity of your approach?

**Answer:**
```python
def is_palindrome(s: str) -> bool:
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]
```
Time: O(n). Space: O(n) for the cleaned copy.

