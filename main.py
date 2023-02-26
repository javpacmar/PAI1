import datetime
import hashlib
import sys
import os

from files import create_files, search_file
from server import run_server

cloud_folder_path = "cloud"
local_folder_path = "local"
index_path = "index"

def help():
    print("Usage: python main.py <command>")
    print("Commands: server, create-files, check, help")
            
def create_mac(hash, token):
    
    # Challenge: Depending on the day of the week, the operation will be different
    today = datetime.datetime.today()
    day = today.weekday()
        
    # Create mac with diferent string operations (challenge)
    if day == 0:
        mac = hashlib.sha256((hash + token).encode()).hexdigest()
    elif day == 1:
        mac = hashlib.sha256((token + hash).encode()).hexdigest()
    elif day == 2:
        mac = hashlib.sha256((hash + token + hash).encode()).hexdigest()
    elif day == 3:
        mac = hashlib.sha256((token + hash + token).encode()).hexdigest()
    elif day == 4:
        mac = hashlib.sha256((hash + token + hash + token).encode()).hexdigest()
    elif day == 5:
        mac = hashlib.sha256((token + hash + token + hash).encode()).hexdigest()
    elif day == 6:
        mac = hashlib.sha256((hash + token + hash + token + hash).encode()).hexdigest()
    
    return mac
    
def check_mac(mac_local, mac_cloud):
    # Compare mac
        if mac_local == mac_cloud:
            print("Macs match")
            return True
        else:
            print("Macs don't match")
            return False
        
def check(file, token):

    local_hash_path = os.path.join(local_folder_path, f"{file}.hash")
    with open(local_hash_path, "r") as f:
        hash=f.read()  
    
    hash_file_path_cloud = search_file(file + ".hash")
    
    if hash_file_path_cloud is None:
        sys.exit(1)
        
    # Open hash file
    with open(hash_file_path_cloud, "r") as f:
        # Read hash file
        hash_file_cloud = f.read()
        # Compare hashes
        print(f"Local hash: {hash}")
        print(f"Cloud hash: {hash_file_cloud}")
        if hash == hash_file_cloud:
            print("Hashes match")
            local_mac = create_mac(hash, token)
            print(f"Local mac: {local_mac}")
            cloud_mac = create_mac(hash_file_cloud, token)
            print(f"Cloud mac: {local_mac}")
            check_mac(local_mac, cloud_mac)
        else:
            print("Hashes don't match")
            print(f"New hash: {hash_file_cloud}")
            return False
        


if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) != 2:
        help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        file = input("Enter file name: ")
        token = input("Enter token: ")
        check(file, token)
    elif command == "create-files":
        total_files = input("Enter files number to create: ")
        create_files(int(total_files))
    elif command == "server":
        run_server()
    elif command == "help":
        help()
    else:
        print("Invalid command")
        help()