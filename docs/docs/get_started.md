---
sidebar_position: 3
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

Designed to be a very user-friendly module, `HydroDB` only has 6 operational functions and 4 observable functions to be called.

## Operational Functions

The opearional functions are thesigned to execute the CRUD 

- C : create
- R : read
- U : update
- D : delete

1 of them are to `create`, 1 for `reade`, 3 for `update` and 1 for `delete`e

    
### create_table() --> `create`

The create() function is designed for the creation of tables, along with the columns that each table possesses.

```python 
hydro.create_table(
    tables="Table_1", 
    columns=["name", "age"],
    pk="name"
)
```

```json
// Expected table structure
{
  "TABLE NAME": "TABLE_1",
  "META DATA": null,
  "TABLE COLUMNS": [
    "name",
    "age",
  ],
  "PK": "name",
  "ROWS": []
}
```
- `tables`: str --> Na name of the table to be created. (Learn more about [strings](https://www.w3schools.com/python/python_strings.asp))

- `columns`: Lists --> The columns for the table. (Learn more about [lists](https://www.w3schools.com/python/python_lists.asp))

- `pk`: str --> Defines the primary key of the table. If no values are passed, the primary-key will be the  `id`


### add_row() --> `update`

To add values to table's columns, uses the add() function.

```python
hydro.add_rows(
    table_name="Table_1",
    into_columns=["name", "age"],
    values=["James", 34]
)
```
```json
// Expected result
{
  "TABLE NAME": "TABLE_1",
  "META DATA": null,
  "TABLE COLUMNS": [
    "name",
    "age",
  ],
  "PK": "name",
  "ROWS": [
    {
        "id": 1,
        "values":{
            "name": "James",
            "age": 34
        }
    }
  ]
}
```

- `tables_names`: str --> Receives the table that you want to add values.

- `into`: list --> These are the columns of the table that will have a value added.

- `values`: list --> These are the values for each column selected.


### querry() --> `search`

This function is used to get values from a table.


```python
hydro.querry(
    from_="Table_1",
    columns=["name", "age"],
    where="age = 34"
)
```

```bash
# expected output: [{"id" : 1, "values" :{"name":"James", "age":34}}]
```
**NOTE:** A string is returned

- `table_name`: str --> Is the name of the table to be querried.

- `columns`: list --> Here, is the values you want to receve. If None, the entire row is returned.

- `filter`: str --> Is the parameter to querry a specific group of elements or a single element. If non filter parameter is passed, the entire table will be returned.


### update() --> `update`

The update funcions serves to update values from rows, or a single row.
If you want to update a single row, uses the element `id` as the filter parameter.

```python
hydro.update(
    from_="Table_1",
    columns=["name", "age"],
    where="name = James"
    with_values=["Caio", 19],
)
```
```json
// Expectd result
{
  "TABLE NAME": "TABLE_1",
  "META DATA": null,
  "TABLE COLUMNS": [
    "name",
    "age",
  ],
  "PK": "name",
  "ROWS": [
    {
        "id": 1,
        "values":{
            "name": "Caio",
            "age": 19
        }
    }
  ]
}
```

- `table_name`:str --> Is the table to update a row, or a group of rows.

- `columns`:list --> These are the list you want to change of each row querried.

- `where`:str --> Specifies the groupe of elements or a single element to be updated.

- `with_values`:list --> The values to be updated to the current row data.

### delete() --> `delete`

This function removes an entire row from the table that has the specified value passed in.

```python
hydro.delete(
    from_="Table_1",
    where="id = 1",
)
```
```json
// Expected result
{
  "TABLE NAME": "TABLE_1",
  "META DATA": null,
  "TABLE COLUMNS": [
    "name",
    "age",
  ],
  "PK": "name",
  "ROWS": []
}
```

- `from_`: str --> Is the table to search the row.

- `where`: str --> pecifies the groupe of elements or a single element to be updated.
