---
sidebar_position: 2
---

# Get Started

Here is a simple guide of how to use the `HydroDB` module


## Calling HydroDB on the program

### Default creation
    To use the module just uses:
```python
from hydrodb import *

hydro = HydroDB()
```
In this case a directory `db/` will be created at yours project folder level
```
your-porject-folder
    |--> db/ 
    |--> hydrodb/
    |--> main.py
```

### Optional dirpath
`HydroDB` allows you to chose a folder to create the database directory

Fot that uses:

```python
from hydrodb import *

hydro = HydroDB(optional_path='any_dir_name')
```

In this case a directory `db/` will be created at yours project folder level

```
your-porject-folder
    |--> any_dir_name
        |--> db/
    |--> hydrodb/
    |--> main.py
```

## Commands list

Thinking to be a very easy module to use, `HydroDB` only has 6 duncions to be called:

### Create()
```python 
    hydro.create(
        tables=["Table_1","Table_2"], 
        columns=(["name", "age"], ["model","year", "value"]),
        primary_key=["name", "model"]
    )

```
- tables:list --> Is the list of tables you want to create in the data base.(know more about [list](https://www.w3schools.com/python/python_lists.asp))

- columns:tuple --> Here the columns are created for eache table. (know more about [tuples](https://www.w3schools.com/python/python_tuples.asp))

- primary_key:list --> Defines the primary key of the table

### Add()
```python
    hydro.add(
        tables_names=["Table_1", "Table_2"],
        into=(["name","age"], ["model","year", "value"]),
        values=(["James","34"], ["Hydro", 2024, "Best"])
    )
```
- tables_names:list --> Recives the tables that you want to add valeus.

- into:tuple --> Those are the columns of eache table that will have a value added.

- values:tuple --> This is the values for eache column selected.