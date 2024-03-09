---
sidebar_position: 2
---

# Get Started

Here is a simple guide on how to use the `HydroDB` module.

## Calling HydroDB in the program

### Default creation
To use the module, simply use:
```python
from hydrodb import *

hydro = HydroDB()
```
In this case, a directory `db/` will be created at your project folder level:
```
your-project-folder
    |--> db/ 
    |--> hydrodb/
    |--> main.py
```

### Optional dirpath
`HydroDB` allows you to choose a folder to create the database directory.

To do that, use:
```python
from hydrodb import *

hydro = HydroDB(optional_path='any_dir_name')
```

In this case, a directory `db/` will be created at your project folder level:
```
your-project-folder
    |--> any_dir_name
        |--> db/
    |--> hydrodb/
    |--> main.py
```

## Commands list

Designed to be a very user-friendly module, `HydroDB` only has 6 functions to be called.


### Create()

The create() function is designed for the creation of tables, along with the columns that each table possesses.

```python 
hydro.create(
    tables=["Table_1", "Table_2"], 
    columns=(["name", "age"], ["model", "year", "value"]),
    primary_key=["name", "model"]
)
```
- `tables`: list --> The list of tables you want to create in the database. (Learn more about [lists](https://www.w3schools.com/python/python_lists.asp))

- `columns`: tuple --> Columns are created for each table. (Learn more about [tuples](https://www.w3schools.com/python/python_tuples.asp))

- `primary_key`: list --> Defines the primary key of the table.


### Add()

To add values to table's columns, uses the add() function.

```python
hydro.add(
    tables_names=["Table_1", "Table_2"],
    into=(["name", "age"], ["model", "year", "value"]),
    values=(["James", "34"], ["Hydro", 2024, "Best"])
)
```
- `tables_names`: list --> Receives the tables that you want to add values.

- `into`: tuple --> These are the columns of each table that will have a value added.

- `values`: tuple --> These are the values for each column selected.


### Quearry()

This function is used to get values from a table.


```python
hydro.update(
    table_name="Table_1",
    columns=["name", "age"],
    filter="model = Hydro"
)
```

```bash
# expected output: [{"model":"Hydro, "year":2024}]
```
**NOTE:** A string is returned

- `table_name`: str --> Is the name of the table to be querried.

- `columns`: list --> Here, is the values you want to receve. If None, the entire row is returned.

- `filter`: str --> Is the parameter to querry a specific group of elements or a single element. If non filter parameter is passed, the entire table will be returned.


### Update()

The update funcions serves to update values from rows, or a single row.
If you want to update a single row, uses the element `id` as the filter parameter.

```python
hydro.update(
    table_name="Table_1",
    columns=["name", "age"],
    values=["Caio", 19],
    filter="name = James"
)
```

- `table_name`:str --> Is the table to update a row, or a group of rows.

- `columns`:list --> These are the list you want to change of each row querried.

- `values`:list --> The values to be updated to the current row data.

- `filter`:str --> Specifies the groupe of elements or a single element to be updated.


### Delete()

This function removes an entire row from the table that has the specified value passed in.

```python
hydro.delete(
    table="Table_1",
    column_to_filter="id",
    value_to_filter=0
)
```

- `table`: str --> Is the table to search the row.

- `column_to_filter`: str --> Receives the column to be used as a filter for the desired row.

- `value_to_filter`: Any --> Here is the value to look up.