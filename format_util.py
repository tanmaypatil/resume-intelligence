import json
from pprint import pprint

def transform_contact_json_to_list(json_data):
    """
    Transform contact information from JSON format to a specific list of lists format.
    
    Args:
        json_data (dict): JSON data containing personal details
        
    Returns:
        list: List of lists containing contact information in the specified format
    """
    personal_details = json_data.get("personalDetails", {})
    
    # Extract values from JSON, using empty string as default
    email = personal_details.get("email", "")
    urls = personal_details.get("personalUrls", [])
    city = personal_details.get("city", "")
    phone = personal_details.get("phone", "")
    
    # Create the list structure
    # First row: email and medium URL (if exists)
    row1 = [email, ""]  # Second element will be medium URL if present
    
    # Second row: first GitHub URL (if exists) and city
    row2 = ["", city]  # First element will be GitHub URL if present
    
    # Third row: phone number and empty string
    row3 = [phone, ""]
    
    # Handle URLs
    for url in urls:
        if "github.com" in url.lower():
            row2[0] = url
        elif "medium.com" in url.lower():
            row1[1] = url
    
    return [row1, row2, row3]

def extract_personal_details(json_data):
    if not (isinstance(json_data,dict)):
      json_dict = json.loads(json_data)
    else:
      json_dict = json_data
    
    # Get personal details dictionary
    personal_details =  json_dict.get("personalDetails", {})
    
    print(json.dumps(personal_details))
    
      # Extract values from JSON, using empty string as default
    email = personal_details.get("email", "")
    urls = personal_details.get("personalUrls", [])
    city = personal_details.get("city", "")
    phone = personal_details.get("phone", "")
    
     
    # Create the list structure
    # First row: email and medium URL (if exists)
    row1 = [email, ""]  # Second element will be medium URL if present
    
    # Second row: first GitHub URL (if exists) and city
    row2 = ["", city]  # First element will be GitHub URL if present
    
    # Third row: phone number and empty string
    row3 = [phone, ""]
    
     # Handle URLs
    for url in urls:
        if "github.com" in url.lower():
            row2[0] = url
        elif "medium.com" in url.lower():
            row1[1] = url
    
    list = [row1, row2, row3]
    
    pprint(list)
    return list 

