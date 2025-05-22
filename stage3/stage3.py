import requests
from http import HTTPStatus

headers = {'Accept-Language': 'en-US,en;q=0.5'}
url_ok = "https://www.facebook.com/"
url_bad = "http://google.com/asdfg"


def get_response():
    response = requests.get(url=url_ok, headers=headers)
    if response.status_code == HTTPStatus.OK:
        return response.content

    else:
        print(f"The URL returned {response.status_code}!")
        return None


def save_to_file(input_data):
    try:
        with open("source.html", 'wb') as file:
            file.write(input_data)
        print("Content saved.")
    except PermissionError:
        print("Error during saving file")


data = get_response()
if data:
    save_to_file(data)

