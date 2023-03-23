import requests
import re
import ast
from bs4 import BeautifulSoup

url_list = []
letters_username = []

with open('url_list.py') as f:
    node = ast.parse(f.read())

for item in node.body:
    if isinstance(item, ast.Assign):
        var_name = item.targets[0].id
        var_value = ast.literal_eval(item.value)
        url_list.append((var_name, var_value))

username = input("Enter Username:- ")
print("\n")
for char in username:
    if char.isalnum():
        letters_username.append(char)

for item in url_list:
    url = item[1].replace("username", username)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_web = soup.title
    if title_web is not None and title_web.string is not None:
        title = title_web.string
        words_list = re.findall(r'\b\w+\b', title.lower())
        words = list(set(words_list))
        for i in range(len(letters_username)):
            updating_name = "".join(letters_username[:i+1]).lower()
            for word in words:
                if updating_name == word.lower():
                    print(item[0],"=>",url)

