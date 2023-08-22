import sys
import requests
import re
from bs4 import BeautifulSoup
import ast

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
END_COLOR = "\033[0m"

# Load URL list from the file 'url_list.py'
url_mappings = []
cleaned_username_chars = []

with open('url_list.py') as f:
    ast_tree = ast.parse(f.read())

# Extract URL variables from parsed AST
for node_item in ast_tree.body:
    if isinstance(node_item, ast.Assign):
        var_name = node_item.targets[0].id
        var_value = ast.literal_eval(node_item.value)
        url_mappings.append((var_name, var_value))

# Get username from user
if len(sys.argv) > 1:
    input_username = sys.argv[1]
    print(f"{BOLD}{GREEN}Checking Usrename on :{END_COLOR} {RED}{input_username}{END_COLOR}{END_COLOR},...")
else:
    input_username = input(f"{YELLOW}Enter Username: {END_COLOR}")
    print(f"{BOLD}{GREEN}Checking Usrename on :{END_COLOR} {RED}{input_username}{END_COLOR}{END_COLOR},...")

# Clean up username to contain only alphanumeric characters
for char in input_username:
    if char.isalnum():
        cleaned_username_chars.append(char)

# Iterate through URL mappings and perform requests
for mapping in url_mappings:
    mapping_name, mapping_url = mapping
    modified_url = mapping_url.replace("username", input_username)
    response = requests.get(modified_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_element = soup.title
    
    # Check if title exists and process it
    if title_element and title_element.string:
        title_text = title_element.string
        words_list = re.findall(r'\b\w+\b', title_text.lower())
        unique_words = set(words_list)
        
        # Check for username substrings in words
        for i in range(len(cleaned_username_chars)):
            current_name_segment = "".join(cleaned_username_chars[:i+1]).lower()
            if current_name_segment in unique_words:
                print(f"{RED}{mapping_name}{END_COLOR} {BLUE}=>{END_COLOR} {GREEN}{modified_url}{END_COLOR}")
