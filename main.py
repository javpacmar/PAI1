import datetime
import hashlib
import sys

def help():
    print("Usage: python main.py <command>")
    print("Commands: create-hash, server")

def create_hash(file):
    # Open file in read mode
    with open(file, "r") as f:
        # Read file
        data = f.read()
        
        # Create hash with sha-1
        hash = hashlib.sha1(data.encode()).hexdigest()
            
        # Print hash
        print(f"Hash: {hash}")
        
        #Create hash file
        with open(f"{file}.hash", "w") as f:
            f.write(str(hash))

def check_hash(file):
    # Open file in read mode
    with open(file, "r") as f:
        # Read file
        data = f.read()
        
        # Create hash with sha-1
        hash = hashlib.sha1(data.encode()).hexdigest()
        
        # Open hash file
        with open(f"{file}.hash", "r") as f:
            # Read hash file
            hash_file = f.read()
            
            # Compare hashes
            if hash == hash_file:
                print("Hashes match")
                return True
            else:
                print("Hashes don't match")
                return False
            
def create_mac(file, token):
    # Challenge: Depending on the day of the week, the operation will be different
    today = datetime.datetime.today()
    day = today.weekday()
    
    # Open file in read mode
    with open(file, "r") as f:
        # Read file
        data = f.read()
        
        # Create hash with sha-1
        hash = hashlib.sha1(data.encode()).hexdigest()
        
        # Create mac with diferent string operations
        if day == 0:
            mac = hashlib.sha1((hash + token).encode()).hexdigest()
        elif day == 1:
            mac = hashlib.sha1((token + hash).encode()).hexdigest()
        elif day == 2:
            mac = hashlib.sha1((hash + token + hash).encode()).hexdigest()
        elif day == 3:
            mac = hashlib.sha1((token + hash + token).encode()).hexdigest()
        elif day == 4:
            mac = hashlib.sha1((hash + token + hash + token).encode()).hexdigest()
        elif day == 5:
            mac = hashlib.sha1((token + hash + token + hash).encode()).hexdigest()
        elif day == 6:
            mac = hashlib.sha1((hash + token + hash + token + hash).encode()).hexdigest()
        
        # Print mac
        print(f"MAC: {mac}")
        
        # Create mac file
        with open(f"{file}.mac", "w") as f:
            f.write(str(mac))


if __name__ == "__main__":
    # Check arguments
    if len(sys.argv) != 2:
        help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create-hash":
        file = input("Enter file path: ")
        create_hash(file)
    elif command == "check":
        file = input("Enter file path: ")
        token = input("Enter token: ")
        if check_hash(file):
            create_mac(file, token)
    else:
        print("Invalid command")
        help()