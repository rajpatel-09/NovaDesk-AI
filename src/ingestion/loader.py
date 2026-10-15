from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_company_documents():
   data_path = Path("data/company_docs")
   loader = DirectoryLoader(
      str(data_path),
      glob="**/*.txt",
      loader_cls=TextLoader,
      loader_kwargs={'encoding' : 'UTF-8'}
   ) 

   return loader.load()
    

