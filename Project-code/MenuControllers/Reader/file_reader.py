import pandas as pd

class File_reader:
    def __init__(self, file:str) -> None:
        self.file = file
        self.data = pd.read_csv(self.file)


 