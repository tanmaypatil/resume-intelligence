from pydantic import BaseModel, Field
from typing import List, Optional

# Define a nested Pydantic model for address
class Address(BaseModel):
    street: str
    city: str
    postal_code: Optional[str] = None  # Optional field

# Define the main model with various types, including lists and nested models
class UserProfile(BaseModel):
    id: int
    name: str
    age: Optional[int] = None  # Optional field
    email: str
    addresses: List[Address]  # A list of Address models
    friends: Optional[List[str]] = []  # A list of strings (optional)
    active: bool = Field(default=True, description="Is the user currently active?")
    roles: List[str] = Field(default_factory=lambda: ["user"])  # Default roles

# Create an instance of the model
profile_data = {
    "id": 1,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "addresses": [
        {"street": "123 Main St", "city": "Wonderland", "postal_code": "12345"},
        {"street": "456 Elm St", "city": "Underland"}  # No postal code provided
    ],
    "friends": ["Bob", "Charlie"],
    "active": True
}

user_profile = UserProfile(**profile_data)

# Print the model instance as a dictionary (use .model_dump() instead of .dict())
print("Model as Dictionary:", user_profile.model_dump())

# Print field names (keys) using .model_fields.keys()
print("\nModel Fields (Keys):", user_profile.model_fields.keys())

# Print detailed information about fields
print("\nDetailed Field Info:")
for field_name, field_info in user_profile.model_fields.items():
    print(f"{field_name}: {field_info}")
