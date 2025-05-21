import requests


headers = {
    'Accept': 'application/json'
}
# example of working id
# joke_id = "R7UfaahVfFd"




def random_joke_request():
    response = requests.get(url="https://icanhazdadjoke.com", headers=headers)
    data = response.json()
    return data["joke"]


def id_joke_request():
        joke_id = input("Input id of joke:\n")
        try:
            response = requests.get(url=f"https://icanhazdadjoke.com/j/{joke_id}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "joke" in data:
                    return data["joke"]
                else:
                    return "Invalid resource"
            else:
                return "Invalid resource!"
        except requests.exceptions.RequestException:
            return "Invalid resource! "



want_random = input("Do you want some random joke or you will try to hit id? yes/no ")
want_random = want_random.lower()

if want_random == "yes":
    print(random_joke_request())
elif want_random == "no":
    print(id_joke_request())
else:
    print("Invalid input. Showing a random joke by default.")
    print(random_joke_request())