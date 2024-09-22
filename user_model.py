from typing import List
from pydantic import BaseModel

# Define a Pydantic model
class User(BaseModel):
    id: int
    name: str
    age: int
    email: str = "example@example.com"  # Default value

# Create an instance of the model
user = User(id=1, name="John Doe", age=30)

# 1. Print the field names (keys)
print("Model Fields (Keys):", user.model_fields.keys())

# 2. Print detailed information about the fields
print("\nDetailed Field Info:")
for field_name, field_info in user.model_fields.items():
    print(f"{field_name}: {field_info}")

# 3. Print the model's configuration (useful metadata like validation settings)
print("\nModel Config:")
print(user.model_config)

# 4. Access the model as a dictionary (all keys and values)
print("\nModel as a dictionary:")
print(user.model_dump())

# Create individual instances of the model
user1 = User(id=1, name="Alice Smith", age=10 , email="alice@example.com")
user2 = User(id=2, name="Bob Johnson", age = 30 ,email="bob@example.com")
user3 = User(id=3, name="Charlie Brown", age = 40 ,email="charlie@example.com")

# Create a list of Pydantic objects
users: List[User] = [user1, user2, user3]

print(users[0].name)
