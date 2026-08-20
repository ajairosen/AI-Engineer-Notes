# Python Interview Questions — Theoretical & Situational

Conceptual "explain this" / "predict the output" / gotcha questions, as distinct from the coding-problem files (`basic.md`, `intermediate.md`, `advanced.md`).

## Q1: Mutable default argument

What's wrong with this function, and what does it actually print?

```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("banana"))
print(add_item("cherry"))
```

**Answer:**

*Output (not three separate one-item lists):*
```
['apple']
['apple', 'banana']
['apple', 'banana', 'cherry']
```

*Why it happens:*
- Default arg values (`basket=[]`) are evaluated **once, when the `def` statement runs** — not on every call — and stored on the function object itself.
- Every call that doesn't pass its own `basket` argument reuses that **same list object**.
- Lists are **mutable**, so `.append()` permanently changes that shared object — the mutation persists into the next call.
- Result: calls that look independent secretly share state, and the list silently keeps growing across calls.
- Passing your own list explicitly (e.g. `add_item("watermelon", basket=[])`) sidesteps the bug — the parameter is bound to a fresh object instead of the shared default.

*Why it matters in production:*
- Not a crash — a **silent correctness bug**. State leaks between calls that should be independent (e.g. a per-request list in a web handler bleeding into the next request), which shows up as unexplainable data mixing or unbounded memory growth in a long-running service.

*Fix — use `None` as a sentinel:*
```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```
Now a fresh list is created *inside* the function body on every call that doesn't pass one in.

## Q2: Shallow copy vs. deep copy

What's the difference between a shallow copy and a deep copy? Predict the output:

```python
import copy

original = [[1, 2, 3], [4, 5, 6]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

original[0][0] = 999

print(shallow)
print(deep)
```

**Answer:**

*Output:*
```
[[999, 2, 3], [4, 5, 6]]
[[1, 2, 3], [4, 5, 6]]
```

*Why:*
- **Shallow copy** (`copy.copy`) makes a new *outer* list, but its elements are the same objects as the original's — the inner lists aren't copied, just referenced. `original[0]` and `shallow[0]` point to the identical list in memory, so mutating one mutates both.
- **Deep copy** (`copy.deepcopy`) recursively copies every nested object too, so `deep[0]` is a completely independent list — mutating `original` never touches it.

*Why it matters in production:*
- Comes up whenever duplicating nested/config-like structures (e.g. a default settings dict with nested lists/dicts) — a shallow copy there is a classic source of "I copied it but it still changed anyway" bugs. Same root mechanism as the mutable-default-argument gotcha in Q1: mutation reaching through a shared reference.

## Q3: `*args` vs. `**kwargs`

What's the difference between `*args` and `**kwargs`? What does this print, and why?

```python
def describe(*args, **kwargs):
    print(args)
    print(kwargs)

describe(1, 2, 3, name="claude", role="assistant")
```

**Answer:**

*Output:*
```
(1, 2, 3)
{'name': 'claude', 'role': 'assistant'}
```

*Why:*
- `*args` collects any extra **positional** arguments (passed without a keyword) into a **tuple**.
- `**kwargs` collects any extra **keyword** arguments (passed as `name=value`) into a **dict**.
- The names `args`/`kwargs` are just convention — it's the `*`/`**` that matters, not the identifier.
- The same mechanism runs in reverse for unpacking at a call site: `f(*some_list)` spreads a list into positional args, `f(**some_dict)` spreads a dict into keyword args — the other half interviewers often follow up on.
