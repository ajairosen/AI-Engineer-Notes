# Pandas Interview FAQ

## Q1: `.loc` vs. `.iloc`

**Answer:**
- **`.loc`** — label-based, slice end is **inclusive**. `df.loc[0:3]` → 4 rows.
- **`.iloc`** — position-based, slice end is **exclusive**. `df.iloc[0:3]` → 3 rows.

## Q2: Top N groups by an aggregate

Given a DataFrame of transactions with columns `user_id` and `amount`, find the top 3 users by total spend.

```python
import pandas as pd

df = pd.DataFrame({
    "user_id": ["a", "b", "a", "c", "b", "a", "d"],
    "amount":  [10,  20,  5,  50,  30,  15,  8]
})
```

**Answer:**
```python
df.groupby('user_id')['amount'].sum().sort_values(ascending=False).head(3)
```
- **Approach:** group by `user_id`, sum `amount` within each group, *then* sort the aggregated totals and take the top 3. Result: `b` (50), `c` (50), `a` (30).
- **Common mistake:** `df.sort_values('amount', ascending=False).head(3)` sorts individual transaction *rows*, not per-user totals — it answers "top 3 single transactions," not "top 3 users by total spend," and can even show the same user's rows more than once instead of distinct users. Always distinguish "top N rows by a column" from "top N groups by an aggregate."

## Q3: Extracting the month from a date column

Given a DataFrame with a `date` column of type string (e.g. `"2026-01-15"`), convert it to a proper datetime type and extract the month into a new column.

**Answer:**
```python
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month    # int: 1-12
```
- **Approach:** `pd.to_datetime` parses the string column into real `datetime64` values, unlocking the `.dt` accessor namespace. `.dt.month` returns the month as an **integer** (1–12), ready for numeric filtering/sorting/grouping.
- **Common mistake:** `.dt.strftime('%m')` also "extracts the month," but returns a **zero-padded string** (`"01"`...`"12"`) instead of a number — fine for display, but wrong dtype if you need numeric comparisons (`month > 6`) or correct chronological sorting rather than lexicographic. Use `.dt.month` for the raw value, `.dt.strftime()` only when you specifically want a formatted string.

## Q4: Left join — keeping all rows from one side

You have `orders` (`order_id`, `user_id`) and `users` (`user_id`, `signup_date`). Get all orders, including orders from users not present in `users` (those should show `NaN` for `signup_date`). Which merge `how` do you use?

```python
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4],
    "user_id":  ["a", "b", "c", "z"]    # "z" has no matching user
})

users = pd.DataFrame({
    "user_id": ["a", "b", "c"],
    "signup_date": ["2025-01-01", "2025-02-15", "2025-03-10"]
})
```

**Answer:**
```python
pd.merge(orders, users, on='user_id', how='left')
```
- **Approach:** `how='left'` keeps every row from the left table (`orders`) regardless of whether a match exists in `users`, filling unmatched columns with `NaN`. `order_id=4` (`user_id="z"`) → `signup_date = NaN`, since `"z"` isn't in `users`.
- **Common mistake:** `how='inner'` (the default) would silently **drop** the unmatched row entirely instead of keeping it with `NaN` — easy to miss if you don't check row counts before/after a merge. Always verify `len(result)` matches expectations after a join.

## Q5: Boolean column from a condition, without `.apply()`

Given a DataFrame of orders with a `status` column, add a boolean column `is_completed` that's `True` only when `status == "completed"` — without using `.apply()`.

```python
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5],
    "status": ["completed", "cancelled", "pending", "completed", "completed"]
})
```

**Answer:**
```python
orders['is_completed'] = orders['status'] == 'completed'
# [True, False, False, True, True]
```
- **Approach:** `==` on a Series is a vectorized element-wise comparison — broadcasts across the whole column and returns a proper boolean Series directly, no loop or `.apply()` needed. This is about as fast as pandas comparisons get.
- **Common mistake:** `orders['status'].apply(lambda x: True if x == 'completed' else x)` has two problems — it uses `.apply()` (a Python-level loop) when a vectorized comparison would do, *and* the `else x` branch returns the original string instead of `False`, producing a mixed-type column (`True`/`"cancelled"`/`"pending"`) instead of a real boolean one. Always define both branches of a boolean condition explicitly.

## Q6: Per-group percentage, keeping original row shape

Given a DataFrame of employees with `department` and `salary`, add a column `salary_pct_of_dept` showing each employee's salary as a percentage of their department's total salary.

```python
employees = pd.DataFrame({
    "name":       ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "department": ["eng", "eng", "sales", "sales", "eng"],
    "salary":     [100, 150, 80, 120, 50]
})
```

**Answer:**
```python
employees['salary_pct_of_dept'] = (
    employees['salary'] / employees.groupby('department')['salary'].transform('sum') * 100
)
```
Result: Alice 33.33%, Bob 50%, Carol 40%, Dave 60%, Eve 16.67% (eng total=300, sales total=200).

- **Approach:** `.groupby(...).transform('sum')` computes the per-group total but **broadcasts it back to every original row** (shape stays `(5,)`), unlike a plain `.groupby(...).sum()` which collapses to one row per group. `.transform()` is the right tool whenever you need a per-group aggregate lined up against the original, un-collapsed DataFrame so it can be assigned as a new column directly.

