---
sidebar_position: 2
---

# About HydroDB

`HydroDB` can be a non-relational or a relational database library for Python, designed to be easy to use and agile. It allows you to create `JSON` files and store data in them with desired keys. Additionally, it enables searching, updating, and deleting data within the `JSON` file.

## Why HydroDB exists?

The idea for HydroDB emerged during my college days when I had to use TinyDB in one of my classes. While TinyDB is a good library for non-relational databases, I felt that something was missing. After studying the subject, I decided to create my own non-relational database library.

## Setting Up

### Requirements (for versions 1.#.#)

- [Python 3](https://www.python.org/downloads/) version 3.12.2 or above.
  - Also, the `yaspin` Python module version 3.0.1 or above. Install it using the following command in the terminal:

```bash
pip install yaspin
```

### Getting the Module

Currently, the `HydroDB` module is not available on PyPI. To use it, you'll need to fork the directory:

- Visit the [HydroDB](https://github.com/CaioTeixeiraDePaula/HydroDB) repository and follow the instructions. You can download the `.zip` file or clone the repository.

### Downloading:

- Navigate to the **tags** section and select the latest version.
- Download the `.zip` file.

### Usage:

To use the library, copy the `hydrodb` directory to your project. The project folder structure should look like this:

```
your-project-dir/
    |--> main.py
    |--> modules/
    |--> hydrodb/
```


```python
from hydrodb import *
# rest of your code
```


## Data structure

On HydroDB all `JSON` files has an shered base struct:

```json
{
  "TABLE NAME": "tables-name",
  "META DATA": "tables-meta-data",
  "TABLE COLUMNS": [
    "columns_1",
    "columns_2",
    "...",
  ],
  "PK": "tables-primary-key",
  "ROWS": [
        {
          "id": 1,
          "values": {
              "column_1": "x",
              "columns_2": null,
          }
        }
  ]
}
```

> - "TABLE TABME": string -> Is the name of the table.
>
> - "META DATA": string -> Here goes the descriptions of the data tha goes into the table. 
>
> - "TABLE COLUMNS":array/list -> The columns tha goes into the table.
>
> - "PK": string -> Is the columns that represents the primary key of the table.
>
> - "ROWS": array/list of dictionaries -> Here goes the rows of the table. Is important to remember that every single row has an id and the values of the row associeted with the table's columns.

## Observable functions
Those functions are made to lookup the table, for general