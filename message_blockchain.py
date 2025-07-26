import hashlib
import json
import os
from datetime import datetime

BLOCKCHAIN_FILE = "blockchain.json"

class Block:
    def __init__(self, index, message, previous_hash, timestamp=None):
        self.index = index
        self.message = message
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.message}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, message):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), message, previous_block.hash)
        self.chain.append(new_block)
        self.save_chain()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def save_chain(self):
        data = []
        for block in self.chain:
            data.append({
                "index": block.index,
                "message": block.message,
                "timestamp": block.timestamp,
                "hash": block.hash,
                "previous_hash": block.previous_hash
            })
        with open(BLOCKCHAIN_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_chain(self):
        if os.path.exists(BLOCKCHAIN_FILE):
            with open(BLOCKCHAIN_FILE, "r") as f:
                data = json.load(f)
                self.chain = []
                for block_data in data:
                    block = Block(
                        block_data["index"],
                        block_data["message"],
                        block_data["previous_hash"],
                        block_data["timestamp"]
                    )
                    # Keep original hash from file
                    block.hash = block_data["hash"]
                    self.chain.append(block)
        else:
            self.chain.append(self.create_genesis_block())
            self.save_chain()

    def print_chain(self):
        for block in self.chain:
            print(f"\nIndex: {block.index}")
            print(f"Message: {block.message}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")

# ------------------ MENU -------------------
def main():
    blockchain = Blockchain()

    while True:
        print("\nOptions:")
        print("1. Add new block")
        print("2. Show blockchain")
        print("3. Verify blockchain")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            msg = input("Enter message: ")
            blockchain.add_block(msg)
            print("Block added!")
        elif choice == "2":
            blockchain.print_chain()
        elif choice == "3":
            print("Blockchain valid?" , blockchain.is_chain_valid())
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
