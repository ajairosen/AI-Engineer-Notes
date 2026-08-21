# NumPy Interview FAQ

## Q1: Rolling (moving) average without pandas

Given a NumPy array of daily sales, compute the N-day rolling average without using pandas.

**Answer:**

*Loop-based (works, O(n·window)):*
```python
import numpy as np

def rolling_average(arr, window=3):
    averages = []
    for i in range(len(arr) - window + 1):
        window_list = arr[i:i + window]
        averages.append(np.average(window_list))
    return np.array(averages)

sales = np.array([120, 85, 90, 200, 150, 60, 175])
print(rolling_average(sales, 3))
# [ 98.33333333 125.         146.66666667 136.66666667 128.33333333]
```

*Vectorized (idiomatic NumPy, no Python loop):*
```python
def rolling_average(arr, window=3):
    return np.convolve(arr, np.ones(window) / window, mode='valid')
```
- **Approach:** `np.convolve` with a uniform weight kernel (`ones(window)/window`) computes a moving average in one vectorized C-level pass; `mode='valid'` keeps only positions where the window fully overlaps the array. Prefer this over an explicit Python loop — same reasoning as avoiding `.iterrows()` in pandas: vectorized operations run as compiled C loops instead of the Python interpreter looping element-by-element.

## Q2: Row-wise normalization

Given a 2D NumPy array, normalize each row so its values sum to 1.

```python
arr = np.array([
    [1, 2, 3],
    [4, 4, 4],
    [10, 0, 0]
])
```

**Answer:**
```python
result = arr / arr.sum(axis=1, keepdims=True)
# [[0.16666667 0.33333333 0.5       ]
#  [0.33333333 0.33333333 0.33333333]
#  [1.         0.         0.        ]]
```
- **Approach:** `arr.sum(axis=1)` collapses each row to a single total (shape `(3,)`), but dividing directly against that would broadcast along the wrong axis. `keepdims=True` keeps the result shape `(3, 1)`, so broadcasting correctly divides each row by its own row-sum instead of misaligning against columns. This `keepdims` gotcha is the same broadcasting-shape reasoning that shows up any time you reduce along one axis and then need to re-combine with the original array.

## Q3: Mean ignoring NaNs, and a NaN mask

Given `arr = np.array([1.0, 2.0, np.nan, 4.0, np.nan, 6.0])`, compute the mean ignoring NaNs, and get a boolean mask of where the NaNs are.

**Answer:**
```python
mean = np.nanmean(arr)    # 3.25  (mean of [1, 2, 4, 6], NaNs excluded)
mask = np.isnan(arr)      # [False, False,  True, False,  True, False]
```
- **Approach:** `np.nanmean` (and the wider `np.nan*` family — `nansum`, `nanstd`, `nanmax`, etc.) skips NaNs automatically instead of propagating them (plain `np.mean` would return `nan` if any element is `nan`). `np.isnan` gives an element-wise boolean mask, usable directly for filtering (`arr[~mask]`) or counting (`mask.sum()`).

## Q4: Top-k indices without a full sort

Given `arr = np.array([5, 1, 9, 3, 7, 2, 8])`, find the indices of the 3 largest values without fully sorting the array.

**Answer:**
```python
indices = np.argpartition(arr, -3)[-3:]
indices = indices[np.argsort(arr[indices])[::-1]]

print(indices)      # [2 6 4]
print(arr[indices]) # [9 8 7]
```
- **Approach:** `np.argpartition(arr, -3)` runs in O(n) average time (introselect) — it only guarantees the 3 largest elements land in the last 3 positions, in *arbitrary* order among themselves, unlike a full `argsort` which is O(n log n) and orders everything. Sorting just that small 3-element slice afterward to get descending order is O(k log k), negligible. Use this pattern whenever you need "top k" or "bottom k" without caring about the order of everything else — a full sort does unnecessary extra work.


