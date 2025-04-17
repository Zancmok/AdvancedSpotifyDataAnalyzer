"""
Chat gpt was used here!
"""


import bcrypt

def generate_hash(password):
    # Converting password to array of bytes 
    bytes = password.encode('utf-8') 

    # Generating the salt 
    salt = bcrypt.gensalt() 

    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)

    print(f"Generated Hash: {hash}")

    return hash  # Return the hash to use in the check_hash function


def check_hash(password, stored_hash):
    # Convert user entered password to bytes
    user_bytes = password.encode('utf-8')

    # Check if entered password matches the stored hash
    if bcrypt.checkpw(user_bytes, stored_hash):
        print("Password is correct!")
    else:
        print("Password is incorrect!")


# Example password 
password = 'bobro-ja-pierdole'

# Generate the hash for the password
# hashed_password = generate_hash(password)

check_hash(password, b'$2b$12$l6uY4uYYf6rofepVb6PshO7ExPnH.7Rmh9NX1gm41CSNsxPqH27ny')

# Now, you can check the hash with the correct password
# check_hash(password, hashed_password)

# You can also test with a wrong password
# wrong_password = 'wrong-password'
# check_hash(wrong_password, hashed_password)
