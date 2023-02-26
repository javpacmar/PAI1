import hashlib
import os
from whoosh.index import open_dir
from whoosh.fields import SchemaClass, TEXT, ID
from whoosh.index import create_in
from whoosh.qparser import QueryParser
import shutil

cloud_folder_path = "cloud"
local_folder_path = "local"
index_path = "index"


class MySchema(SchemaClass):
    path = ID(stored=True, unique=True)
    content = TEXT(stored=True)


def create_files(total_files):

    if not os.path.exists(cloud_folder_path):
        os.mkdir(cloud_folder_path)
    
    if not os.path.exists(local_folder_path):
        os.mkdir(local_folder_path)

    for i in range(1, total_files + 1):
        filename = f"file{i}.txt"
        print(f"Creating {filename}...")
        
        cloud_file_path = os.path.join(cloud_folder_path, filename)      

        with open(cloud_file_path, "w") as f:
            f.write(f"This is the file {i}")
        
        with open(cloud_file_path, "r") as f:
            hash = hashlib.sha256(f.read().encode()).hexdigest()
            
            #Create hash file
            with open(f"{cloud_file_path}.hash", "w") as f:
                f.write(str(hash))
            #Hash only in local    
            local_hash_path = os.path.join(local_folder_path, f"{filename}.hash")
            with open(local_hash_path, "w") as f:
                f.write(str(hash))     

    if not os.path.exists(index_path):
        os.mkdir(index_path)
        ix = create_in(index_path, MySchema)
    else:
        ix = open_dir(index_path)

    writer = ix.writer()

    for subdir, dirs, files in os.walk(cloud_folder_path):
        for file in files:
            filepath = os.path.join(subdir, file)

            doc = {'path': filepath, 'content': file}
            writer.add_document(**doc)

    writer.commit()

def search_file(filename):

    ix = open_dir(index_path)

    query_parser = QueryParser("content", schema=ix.schema)

    query = query_parser.parse(filename)

    with ix.searcher() as searcher:
        results = searcher.search(query)

        for r in results:
            print("Found " + r["path"])
        
        if len(results) == 0:
            print("File not found")
            return None
    
        return results[0]["path"]
