from os.path import exists, getsize
from os import mkdir, getcwd
from .visuals import *
import json
from datetime import datetime


class HydroDB:
    """### Class to handle data with non linked tables

    `Note`: on future updates linked tables will be possible to be manipulated
    """
    def __init__(self,optional_path:str=None, db_name:str="db", default_dir_path:str = getcwd()) -> None:
        
        start_spiner("Creating DB dir")
        self.default_dir_path = default_dir_path.replace("\\", "/")
        
        _create_dir(optional_path=optional_path, db_name=db_name, default_dir_path=self.default_dir_path)
        
        if optional_path:
            self.default_dir_path += f"/{optional_path}"

    
    def create(self, tables:list, columns:tuple=None, primary_key:list=["id"]) -> None:
        """### Fuction used to create the tables with theirs columns

        The list of tables tells the functions the ammount of tables to be created and with theirs names. 
        The tuple of columns tells the function the wich column will go into the owner table.
        All tables have the same base struct:
        \
        {
            "table_name": table_name --> str,
            "meta_data": None --> str,
            "table_columns": ["id"] + columns --> int,
            "rows": [] --> list
        }

        Note: primary_key is for future updates
        """
        _create_table(tables_names=tables, columns=columns, db_dir_path=self.default_dir_path, primary_key=primary_key)

    
    def add(self, tables_names:list , into:tuple, values:tuple):
        """### Adds values to the ctables
        """
        if tables_names is str:
            tables_names = _to_list(tables_names)

        try:
            for table_index in range(len(tables_names)):

                into[table_index].append("id")
                
                table_name = tables_names[table_index]

                values[table_index].append(len(_get_rows(table_name=table_name, db_dir_path=self.default_dir_path))) # Implements the id number by the number of rows in the table

                table_columns = _get_columns(table_name=table_name, db_dir_path=self.default_dir_path)

                row_dict = {}

                row_dict.update({column: None for column in table_columns}) # Initialize with None for all columns

                column = into[table_index]
                value = values[table_index]

                for i in range(len(into[table_index])):
                    if column[i] in row_dict:
                        row_dict[column[i]] = value[i]
                    else:
                        print(f"Column {column[i]} not found in table {tables_names}")
            
                _open_to_write(table_name=table_name, db_dir_path=self.default_dir_path, data_to_write=row_dict, data_index="rows")
            
            success_message("Data added with success")

        except Exception as e:
            fail_message(f"{e}")


    def querry(self, table:str, columns:list=None, filter:str=None):
        """### Function used to search values from tables
        
        #### Params ####
        
        @ list(tables = ...)   -> recives the tables names
        @ tuple(columns = ...) -> recives the columns names for eache table
        @ tuple(filters = ...) -> recives the filters to be used in the querry

        
        The values can be filtered dependding on the demand
        """

        filtered_table:dict = {}

        if filter is None:
            filtering = _search(table_name= table, columns= columns, db_dir_path=self.default_dir_path, data_index='rows')
        else:
            filtering = _search(table_name= table, columns= columns, db_dir_path= self.default_dir_path, filter=filter, data_index='rows')

        filtered_table = filtering

        return filtered_table 
    

    def update(self, table:str, columns:list, values:list, filter:str):
        """### Updates
        """
        
        rows_to_update = self.querry(table=table, columns=columns, filter=filter)

    
    def delete(self, table:str, column_to_filter:str, value_to_filter:str):
        """### Deletes a row from the table

        Note: tries to pass a column that has a unique value, or sometimes an error can appear
        """
        rows_to_delete = self.querry(table=table, filter=f"{column_to_filter} = {value_to_filter}")

        if not rows_to_delete:
            print("No matching rows found to delete.")
            return

        table_data = _open_to_read(table_name=table, db_dir_path=self.default_dir_path, data_index="rows")

        new_table_data = [row for row in table_data if row not in rows_to_delete]

        with open(f"{self.default_dir_path}/db/{table}.json", "w") as table_file:
            json.dump({"table_name": table, "meta_data": None, "table_columns": _get_columns(table, self.default_dir_path), "pk": "id", "rows": new_table_data}, table_file, indent=4)

        print(f"Rows with {column_to_filter}={value_to_filter} deleted successfully.")


    def get_table(self, table_name:str)->dict:
        table_rows = _open_to_read(table_name=table_name, db_dir_path=self.default_dir_path)
        return table_rows    
    

    def teste(self):
        test = _open_to_read(table_name="Positions", db_dir_path=self.default_dir_path, data_index='rows')
        print(test)


#==========================================================================================================================================#
def _get_columns(table_name:str=None, db_dir_path:str=getcwd())->json:
    return _open_to_read(table_name=table_name, db_dir_path=db_dir_path, data_index="table_columns")


def _get_rows(table_name:str=None, db_dir_path:str=getcwd())->json:
    return _open_to_read(table_name=table_name, db_dir_path=db_dir_path, data_index="rows")


def _open_to_read(table_name: str, db_dir_path: str = getcwd(), data_index: str = None):
    if data_index is not None:
        file_path = f"{db_dir_path}/db/{table_name}.json"
        try:
            if not exists(file_path) or getsize(file_path) == 0:
                # If the file is empty or doesn't exist, return an empty result
                return []
            
            with open(file_path, "r+") as raw_table:
                table = json.load(raw_table)
            return table[data_index]
        except json.decoder.JSONDecodeError:
            # Handle the case where the file is not a valid JSON
            return []
    else:
        file_path = f"{db_dir_path}/db/{table_name}.json"
        try:
            if not exists(file_path) or getsize(file_path) == 0:
                # If the file is empty or doesn't exist, return an empty result
                return []
            
            with open(file_path, "r+") as raw_table:
                table = json.load(raw_table)
            return table
        except json.decoder.JSONDecodeError:
            # Handle the case where the file is not a valid JSON
            return []
    


def _open_to_write(table_name: str, db_dir_path: str = getcwd(), data_index: str = None, data_to_write: dict = {})->dict:
    """ Opens json to write data

    Get the table name in the db dir, adds data.
    If a index is passed, it will select the index to write the data.
    
    """
    check = _open_to_read(table_name=table_name, db_dir_path=db_dir_path, data_index=data_index)

    if data_to_write in check: return

    try:
        if data_index is not None:
            with open(f"{db_dir_path}/db/{table_name}.json", "r+") as raw_table:
                __temp_table = json.load(raw_table)
                __temp_table[data_index].append(data_to_write)

            with open(f"{db_dir_path}/db/{table_name}.json", "w") as raw_table:
                json.dump(__temp_table, raw_table, indent=4)

        else:
            with open(f"{db_dir_path}/db/{table_name}.json", "r+") as raw_table:
                __temp_table = json.load(raw_table)
                __temp_table.append(data_to_write)

            with open(f"{db_dir_path}/db/{table_name}.json", "w") as raw_table:
                json.dump(__temp_table, raw_table, indent=4)

    except Exception as e:
        fail_message(f"{e}")


def _create_dir(optional_path:str, db_name:str, default_dir_path:str) -> None:
    """ Creates the db directory
    """
    if ( optional_path ):
        sub_dirs = optional_path.split("/")
        for sub_dir in sub_dirs:
            default_dir_path += f"/{sub_dir}"
            text_marker(default_dir_path)
            sleep(1)
            if not exists(default_dir_path):
                mkdir(default_dir_path)
                success_message("Database directory created with success")
            else:
                fail_message("Directory oready exists")


        try:
            default_dir_path += f"/{db_name}"
            mkdir(default_dir_path)
        except Exception as e:
            fail_message(str(e))

    else:
        default_dir_path += f"/{db_name}"
        try:
            mkdir(default_dir_path)
        except Exception as e:
            fail_message(str(e))
        

def _create_table(tables_names:list, columns:tuple=None, primary_key:list=["id"], db_dir_path:str=None) -> None:
    """ Creates the db tables

    primary_key is for future updates
    """
    if tables_names is str:
        tables_names = _to_list(tables_names)

    for i in range(len(tables_names)):

        temp_dict:dict = {} 
        if columns[i] != None and not exists(f"{db_dir_path}/db/{tables_names[i]}.json"):
            start_spiner("Trying columns")
            if columns is not tuple :
                temp_dict = _create_json_struct(table_name=tables_names[i],columns=columns[i], primary_key=primary_key[i])
            else :
                temp_dict =_create_json_struct(table_name=tables_names[i],columns=columns, primary_key=primary_key)
            try:
                with open(f"{db_dir_path}/db/{tables_names[i]}.json", "w") as table:
                    if exists(f"{db_dir_path}/db/{tables_names[i]}.json") and temp_dict == table:return
                    else:json.dump(temp_dict, table, indent=4)
            except Exception as e:
                fail_message(f"{e}",1)
        else:
            fail_message("Tables exists")


def _create_json_struct(table_name: str, columns: list, primary_key:str) -> dict:
    """Creates the default table structure


    """

    default_json_struc: dict = {
        "table_name": table_name,
        "meta_data": None,
        "table_columns": ["id"] + columns,
        "pk" : primary_key,
        "rows": []
    }

    return default_json_struc


def _search(table_name:str= None, columns:list= None, db_dir_path:str=getcwd(), data_index:str=None, filter:str=None):
    table_to_querry = _open_to_read(table_name=table_name, db_dir_path=db_dir_path, data_index=data_index)

    checker:list = []
    start_spiner("Cheking columns")
    try:
        return _match_filter_command(table_to_filter=table_to_querry, command=filter, columns=columns)



    except Exception as e:
        fail_message(f"{e}")


def _match_filter_command(table_to_filter: dict, command: str, columns: list) -> dict:

    splited_command = command.split(" ")

    column = splited_command[0]
    operator = splited_command[1]
    value_to_filter = splited_command[2]

    if value_to_filter.isnumeric():
        value_to_filter = float(value_to_filter)

    filtered_table = []
    for row in table_to_filter:
        match operator:
            case "=":
                if column in row and value_to_filter == row[column]:
                    if columns:
                        filtered_table.append({i: row[i] for i in columns})
                    else:
                        filtered_table.append(row)

            case "!=":
                if column in row and value_to_filter != row[column]:
                    if columns:
                        filtered_table.append({i: row[i] for i in columns})
                    else:
                        filtered_table.append(row)

            case ">":
                if column in row and float(value_to_filter) > float(row[column]):
                    if columns:
                        filtered_table.append({i: row[i] for i in columns})
                    else:
                        filtered_table.append(row)

            case "<":
                if column in row and float(value_to_filter) < float(row[column]):
                    if columns:
                        filtered_table.append({i: row[i] for i in columns})
                    else:
                        filtered_table.append(row)

            case ">=":
                if column in row and float(value_to_filter) >= float(row[column]):
                    if columns:
                        filtered_table.append({i: row[i] for i in columns})
                    else:
                        filtered_table.append(row)

            case "<=":
                if column in row and float(value_to_filter) <= float(row[column]):
                    if columns:
                        filtered_table.append({i: row[i] for i in columns})
                    else:
                        filtered_table.append(row)

            case None:
                pass

    return filtered_table


def _to_list(_el):
    return [_el]

def _to_tuple(_el):
    return (_el)




"""#Você
Foi embananado

```python
def banana(você:str):
    print(você)
```
"""