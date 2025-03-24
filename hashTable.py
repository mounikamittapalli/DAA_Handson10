import math

# Node for the doubly linked list
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None  # Previous node
        self.next = None  # Next node

# Hash Table class
class HashTable:
    def __init__(self, initial_capacity=5):
        self.capacity = initial_capacity  # Initial size of the hash table
        self.size = 0  # Number of elements in the hash table
        self.table = [None] * self.capacity  # Table for chaining (array of linked lists)

    # Hash function using the multiplication method
    def mul_hash(self, key):
        A = (math.sqrt(5) - 1) / 2  # A ≈ 0.6180339887 (golden ratio conjugate)
        frac_part = (key * A) % 1  # Get the fractional part
        index = int(self.capacity * frac_part)  # Map to table size
        #print(f"[Multiplication] Key: {key}, Index: {index}")
        return index

    # Hash function using the division method
    def div_hash(self, key):
        div = key % self.capacity  # Use modulo operation to get index
        #print(f"[Division] Key: {key}, Index: {div}")
        return div

    # Resize the hash table: grow or shrink based on the load factor
    def resize(self):
        load_factor = self.size / self.capacity

        # Grow the table if the load factor exceeds 75%
        if load_factor >= 0.75:
            new_capacity = self.capacity * 2
        # Shrink the table if the load factor is below 25% and capacity is greater than 8
        elif load_factor <= 0.25 and self.capacity > 8:
            new_capacity = self.capacity // 2
        else:
            return  # No resizing needed

        # Create a new table with the new capacity
        new_table = [None] * new_capacity
        old_table = self.table
        self.table = new_table
        self.capacity = new_capacity
        self.size = 0  # Reset size before rehashing

        # Rehash all elements into the new table
        for node in old_table:
            current = node
            while current:
                # Insert each element into the new table
                self._insert_no_resize(current.key, current.value)
                current = current.next

    # Helper function to insert an element without triggering resize
    def _insert_no_resize(self, key, value, use_mul_hash=True):
        # Select hash function
        if use_mul_hash:
            index = self.mul_hash(key)  # Get the index using multiplication hash function
        else:
            index = self.div_hash(key)  # Get the index using division hash function

        current = self.table[index]

        # Check if the key already exists and update it
        while current:
            if current.key == key:
                current.value = value  # Update the value if key exists
                return
            current = current.next

        # If the key doesn't exist, insert a new node at the head of the list
        new_node = Node(key, value)
        if self.table[index] is not None:
            self.table[index].prev = new_node  # Link the previous head to the new node
        new_node.next = self.table[index]  # Link the new node to the head
        self.table[index] = new_node  # Set the new node as the head of the chain

        self.size += 1

    # Insert a key-value pair into the hash table
    def insert(self, key, value, use_mul_hash=True):
        index = self.mul_hash(key) if use_mul_hash else self.div_hash(key)  # Get the index using chosen hash function
        current = self.table[index]

        # Check if the key already exists and update it
        while current:
            if current.key == key:
                current.value = value  # Update the value if key exists
                return
            current = current.next

        # If the key doesn't exist, insert a new node at the head of the list
        new_node = Node(key, value)
        if self.table[index] is not None:
            self.table[index].prev = new_node  # Link the previous head to the new node
        new_node.next = self.table[index]  # Link the new node to the head
        self.table[index] = new_node  # Set the new node as the head of the chain

        self.size += 1
        self.resize()  # Resize if necessary

    # Search for a key in the hash table and return its value
    def search(self, key):
        index = self.mul_hash(key)  # Get the index using hash function
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None  # Return None if key not found

    # Remove a key-value pair from the hash table
    def remove(self, key):
        index = self.mul_hash(key)  # Get the index using hash function
        current = self.table[index]
        while current:
            if current.key == key:
                # Remove the node from the chain
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.table[index] = current.next  # Head of the chain

                if current.next:
                    current.next.prev = current.prev

                self.size -= 1
                self.resize()  # Resize if necessary
                return True
            current = current.next
        return False  # Return False if key not found

    # Display the contents of the hash table
    def display(self):
        for i in range(self.capacity):
            current = self.table[i]
            if current:
                print(f"Index {i}: ", end="")
                while current:
                    print(f"[{current.key} : {current.value}] ", end="")
                    current = current.next
                print()

# Test the HashTable class
if __name__ == "__main__":
    ht = HashTable()

    # Insert some key-value pairs
    print("Inserting elements:")
    ht.insert(10, 100, use_mul_hash=True)
    ht.insert(20, 200, use_mul_hash=True)
    ht.insert(30, 300, use_mul_hash=True)
    ht.insert(40, 400, use_mul_hash=True)
    ht.insert(50, 500, use_mul_hash=True)
    ht.display()

    # Search for a key
    print(f"\nSearch for key 30: {ht.search(30)}")

    # Remove a key
    print("Removing key 30:")
    ht.remove(30)
    ht.display()

    # Check if the key was removed
    print(f"\nSearch for key 30 after removal: {ht.search(30)}")
