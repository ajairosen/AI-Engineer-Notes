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

## Q2: Decorator vs. decorator factory

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

