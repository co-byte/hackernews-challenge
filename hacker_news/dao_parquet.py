import pyarrow as pa
import pyarrow.parquet as pq
import os

class DaoParquet():

    def __init__(self, parquet_folder: str, parquet_base_filename: str,schema: pa.schema) -> None:
        self.parquet_folder = parquet_folder
        self.base_filename = parquet_base_filename
        self.schema = schema
        self.__counter = 0

    # Only public function
    def save_data(self, data: list[dict]):      
        formatted_data = self.__format_data(data)
        cleaned_data = self.__clean_data(formatted_data)
        table = self.__create_table(cleaned_data)
        self.__write_table(table)

    # Private functions
    def __format_data(self, data: list[dict])-> list[dict]:
        formatted_data = [{key: item.get(key,None) for key in self.schema.names} for item in data]
        return formatted_data

    def __clean_data(self, data: list[dict]):
        # Further functionalities to actually clean the data can be added here
        # Due to time constraints, I was not able to implement this
        return data

    def __create_table(self, data: dict):
        table = pa.Table.from_pydict({key: [item[key] for item in data] for key in self.schema.names}, 
                                     schema=self.schema)
        return table

    def __write_table(self, table: pa.Table):
        if not self.__parquet_folder_exists(self.parquet_folder):
            os.makedirs(self.parquet_folder)

        file_name = f"{self.base_filename}_{self.__counter}.parquet"
        file_location = os.path.join(self.parquet_folder, file_name)

        pq.write_table(table, file_location)
        self.__counter += 1

    @staticmethod
    def __parquet_folder_exists( file_location):
        return os.path.exists(file_location)
    