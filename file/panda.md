# header

```python
# 获取表header
csv_header = list(pd.read_csv(csv_file, nrows=1).columns)

Cov = pd.read_csv("path/to/file.txt", 
                  sep='\t', 
                  names=["Sequence", "Start", "End", "Coverage"])

```

- https://stackoverflow.com/questions/34091877/how-to-add-header-row-to-a-pandas-dataframe

---
# filter

```python
df.loc[df['column_name'].isin(some_values)]
```

- https://stackoverflow.com/questions/17071871/how-to-select-rows-from-a-dataframe-based-on-column-values

