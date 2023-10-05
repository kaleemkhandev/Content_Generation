from langchain.document_loaders.csv_loader import CSVLoader


loader = CSVLoader(file_path="docs/csv/training-Sheet1.csv")

data = loader.load()
a=0