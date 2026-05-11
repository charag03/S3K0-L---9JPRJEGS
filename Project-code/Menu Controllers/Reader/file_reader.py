import pandas as pd

class File_reader:
    def __init__(self, file:str) -> None:
        self.file = file

    def read_file(self) -> pd.DataFrame:
        data = pd.read_csv(self.file)
        return data
 