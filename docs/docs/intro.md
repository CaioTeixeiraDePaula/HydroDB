---
sidebar_position: 1
---

# About HydroDB

`HydroDB` is a non-relation database librarie for python, thought to be easy to use and agile. It allows you yo create `JSON` files and storage data on them, with the desired keys, as well as allows to search data, update and delete data of the `JSON` file

## Why HydroDB Exists

The idea of HydroDB surged when i was at college and in one class we had to use TinyDB. I cant argue that TinyDB isn't a good lib for non-relational database, but i felt something was missing. 
After studing, I decided to create my on non-relational databe lib.

## Seting up 

### What do you need (for version 0.1.0)

- [Python 3](https://www.python.org/downloads/) version 3.12.2 or above:
  - And `yaspin`python mcolude at version 3.0.1 or above. For that use the following command on terminal:

```bash
  pip install yaspin
```

### Getting the module

Right now the `HydroDB` module isn't on pip, so to uses it you'll have to fork the directory :(

- Go to [HydroDB](https://github.com/CaioTeixeiraDePaula/HydroDB) repository and follow the instructios. In this case you can download the `.zip` file or clone the repository

### Downloading:

- Go to **tags** ad chose the laste version that appears
- Download the `.zip` file

### Using:

To use the lib just copy the `hydrodb` directory to your project
> The project folders structure shoul be like this:

    you-project-dir/
        |--> main.py
        |--> modules/
        |--> hydrodb/

- Into `main.py` to import, just uses the ``` from hydrodb import *```. Shoul be like that
```python
from hydrodb import *

# rest of your code

```