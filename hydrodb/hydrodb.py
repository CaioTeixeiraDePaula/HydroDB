from os import getcwd, mkdir
from os.path import exists, getsize
from .visuals import *
import json



class HydroDB:
    def __init__(self, optinoal_db_dir=None) -> None:
        raw_db_dir = getcwd()
        self.db_dir = raw_db_dir.replace('\\', '/')

        _create_db_dir(self.db_dir, optional_path=optinoal_db_dir)

        if optinoal_db_dir:
            self.db_dir += f"/{optinoal_db_dir}/db"
        else:
            self.db_dir +='/db'



    #================================================================================#
    #============================ Operational functions =============================# 
    #================================================================================#
    def create_table(self, table_name:str, columns:list, pk:str) -> None:
        """Creates a table, on DB dir, with the seted columns"""
        
        _create_table(path=self.db_dir, table_name=table_name, columns=columns, pk=pk)


    def add_rows(self, table_name:str, into_columns:list, values:list) -> None:
        """Adds rows to a table, with the seted values, in the seted table's columns"""
        
        row:dict = {}

        table_columns = _read_columns(path=self.db_dir, table_name=table_name)

        for column, value in zip(into_columns,values):
            if column not in table_columns:
                text_marker(f"Columns '{column}' does not exists on table '{table_name}'", "^")
            else:
                row.update({column : value})

        _write_rows(path=self.db_dir, table_name=table_name, row_to_write=row)

    
    def querry(self, from_:str, columns:list, where:str): 
        """Search data from the table"""
        return _match_querry_command(path=self.db_dir, table_name=from_, columns=columns, where=where)
    

    def update(self, from_:str, columns:list, where:str, with_values:list):
        """Updates a row with passed values"""
        _update_row(path=self.db_dir, table_name=from_, command=where, columns=columns, values=with_values)


    def delete(self, from_:str, where:str):
        """Deletes a ros fom a table"""
        _delete_row(path=self.db_dir, table_name=from_, command=where)



    #================================================================================#
    #============================ Observable functions ==============================# 
    #================================================================================#
    def read_table(self, table_name:str) -> dict:
        """Returns the entire table dictionary"""

        return _read_table(path=self.db_dir, table_name=table_name)
    
    def read_rows(self, table_name:str) -> list:
        """Returns the rows of a table"""

        return _read_rows(path=self.db_dir, table_name=table_name)
    
    def read_columns(self, table_name:str) -> list:
        """Returns the columns in a table"""

        return _read_columns(path=self.db_dir, table_name=table_name)


#-------------------------------------#
#          Strict functions           #              
#-------------------------------------#


def _create_db_dir(path:str, optional_path:str) -> None:
    db_dir:str = path
    try:
        if optional_path:
            splited_sec_path:list = optional_path.split('/')
        
            for partial_path in splited_sec_path:
                db_dir += f'/{partial_path}'
                mkdir(db_dir)

        db_dir += "/db"

        mkdir(db_dir)    

    except FileExistsError as e:
        fail_message(f'{e}')


def _create_table(path:str, table_name:str, columns:list, pk:str='id') -> None:

    default_table_struct:dict = {
        "TABLE NAME" : table_name,
        "META DATA" : None,
        "TABLE COLUMNS" : columns,
        "PK" : pk,
        "ROWS" : []
    }

    table_path:str = path + "/" + table_name

    if exists(table_path+'.json'):
        text_marker(f'Table {table_name} exists')
    else:
        start_spiner(f"Creating table : `{table_name}`")
        try:
            with open(table_path+'.json', 'w+') as table_file:
                json.dump(default_table_struct, table_file, indent=4)
        except FileNotFoundError as e:
            fail_message(f'{e}')


def _read_table(path:str, table_name:str) -> dict:
    table_file_path = f"{path}/{table_name}.json"

    try:
        with open(table_file_path, "r") as table_file:
            readed_table = json.load(table_file)
            return readed_table
    except FileNotFoundError:
        print(f"Error: Table file '{table_file_path}' not found.")
    except Exception as e:
        print(f"Error: Failed to read table '{table_file_path}': {e}")



def _read_rows(path:str, table_name:str) -> list:
    return _read_table(path=path, table_name=table_name)["ROWS"]


def _read_columns(path:str, table_name:str) -> list:
    return _read_table(path=path, table_name=table_name)['TABLE COLUMNS']


def _write_rows(path:str, table_name:str, row_to_write:dict):

    row_id = len(_read_rows(path=path, table_name=table_name)) + 1

    data_to_write:dict = {
        "id" : row_id,
        "values" : row_to_write
    }

    with open(f"{path}/{table_name}.json", "r+") as raw_table:
                __temp_table = json.load(raw_table)
                __temp_table["ROWS"].append(data_to_write)

    with open(f"{path}/{table_name}.json", "w") as raw_table:
        json.dump(__temp_table, raw_table, indent=3)
        

def _match_querry_command(path:str, table_name:str, columns:list, where:str) -> list:

    table = _read_table(path=path, table_name=table_name)
    splited_command = where.split(' ')

    column_to_filter:str = splited_command[0]
    commander:str = splited_command[1]
    value_to_filter:str = splited_command[-1]

    if value_to_filter.isnumeric() == True:
        value_to_filter = float(value_to_filter)

    match column_to_filter:
        case "id":
            return _search_from_id(table=table, columns=columns, value_to_filter=value_to_filter, command=commander)
        case _:
           return _search_from_any_colum(table=table, columns=columns, column_to_filter=column_to_filter, value_to_filter=value_to_filter, command=commander)


def _search_from_id(table: dict, columns: list, value_to_filter: str, command: str) -> None:
    rows = table["ROWS"]

    filtered_table = []

    for row in rows:
        row_values = row["values"]
        row_dict = {
            "id": row['id'],
            "values": {}
        }

        match command:
            case '=':
                if row["id"] == value_to_filter:
                    if columns is not None:
                        for column in columns:
                            row_dict["values"][column] = row_values[column]
                    else:
                        row_dict["values"].update(row_values)
                    filtered_table.append(row_dict)

            case "!=":
                if row["id"] != value_to_filter:
                    if columns is not None:
                        for column in columns:
                            row_dict["values"][column] = row_values[column]
                    else:
                        row_dict["values"].update(row_values)
                    filtered_table.append(row_dict)

            case ">":
                if row["id"] > value_to_filter:
                    if columns is not None:
                        for column in columns:
                            row_dict["values"][column] = row_values[column]
                    else:
                        row_dict["values"].update(row_values)
                    filtered_table.append(row_dict)
            
            case "<":
                if row["id"] < value_to_filter:
                    if columns is not None:
                        for column in columns:
                            row_dict["values"][column] = row_values[column]
                    else:
                        row_dict["values"].update(row_values)
                    filtered_table.append(row_dict)
            
            case ">=":
                if row["id"] >= value_to_filter:
                    if columns is not None:
                        for column in columns:
                            row_dict["values"][column] = row_values[column]
                    else:
                        row_dict["values"].update(row_values)
                    filtered_table.append(row_dict)

            case "<=":
                if row["id"] <= value_to_filter:
                    if columns is not None:
                        for column in columns:
                            row_dict["values"][column] = row_values[column]
                    else:
                        row_dict["values"].update(row_values)
                    filtered_table.append(row_dict)

    return filtered_table



def _search_from_any_colum(table:dict, columns:list, column_to_filter:str, value_to_filter:str, command:str):
    rows = table["ROWS"]

    filtered_table:list = []

    for row in rows:
        row_values = row["values"]
        row_dict = {
            "id" : row['id'],
            "values" : {}
        }

        filter_column_value:... = row_values[column_to_filter]

        match command:

            case "=":
                if filter_column_value == value_to_filter:
                    if columns is not None:
                        for column in columns:
                            row_dict["values"][column] = row_values[column]
                    else:
                        row_dict["values"].update(row_values)
                    filtered_table.append(row_dict)

            case "!=":
                if filter_column_value != value_to_filter:
                    if filter_column_value == value_to_filter:
                        if columns is not None:
                            for column in columns:
                                row_dict["values"][column] = row_values[column]
                        else:
                            row_dict["values"].update(row_values)
                        filtered_table.append(row_dict)
                    
            case ">":
                if filter_column_value > value_to_filter:
                    if filter_column_value == value_to_filter:
                        if columns is not None:
                            for column in columns:
                                row_dict["values"][column] = row_values[column]
                        else:
                            row_dict["values"].update(row_values)
                        filtered_table.append(row_dict)
            
            case "<":
                if filter_column_value < value_to_filter:
                    if filter_column_value == value_to_filter:
                        if columns is not None:
                            for column in columns:
                                row_dict["values"][column] = row_values[column]
                        else:
                            row_dict["values"].update(row_values)
                        filtered_table.append(row_dict)

            case ">=":
                if filter_column_value >= value_to_filter:
                    if filter_column_value == value_to_filter:
                        if columns is not None:
                            for column in columns:
                                row_dict["values"][column] = row_values[column]
                        else:
                            row_dict["values"].update(row_values)
                        filtered_table.append(row_dict)
                    
            case "<=":
                if filter_column_value <= value_to_filter:
                    if filter_column_value == value_to_filter:
                        if columns is not None:
                            for column in columns:
                                row_dict["values"][column] = row_values[column]
                        else:
                            row_dict["values"].update(row_values)
                    filtered_table.append(row_dict)

    
    return filtered_table


def _delete_row(path:str, table_name:str, command:str) -> ... :
    rows_to_delete:list = _match_querry_command(path=path, table_name=table_name, columns=None, where=command)

    table_to_remove_rows:dict = _read_rows(path=path, table_name=table_name)

    updated_table_rows:list = []

    for row in table_to_remove_rows:
        if row not in rows_to_delete:
            updated_table_rows.append(row)
    
    table_path:str  = f"{path}/{table_name}.json"

    with open(table_path, "r+") as table_file:
        table:dict = json.load(table_file)
        table["ROWS"] = updated_table_rows

    with open(table_path, 'w') as table_to_write:
        json.dump(table, table_to_write, indent=4)


def _update_row(path:str, table_name:str, command:str, columns:list, values:list) -> None:
    rows_to_update = _match_querry_command(path=path, table_name=table_name, columns=None, where=command)

    table_path = f"{path}/{table_name}.json"

    # _delete_row(path=path, table_name=table_name, command=command)

    with open(table_path, "r+") as table_file:
        table = json.load(table_file)

        for row in rows_to_update:
            for i, table_row in enumerate(table["ROWS"]):
                if table_row["id"] == row["id"]:
                    for column, value in zip(columns, values):
                        table["ROWS"][i]["values"][column] = value

    with open(table_path, "w") as table_file:
        json.dump(table, table_file, indent=4)

    print("Rows updated successfully.")