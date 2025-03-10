from pprint import pprint as pp
import requests


def get_api_data(url):
    """
    Get data from an API

    Args:
        url (str): The URL of the API

    Returns:
        json_response (dict): The JSON response from the API
    """
    try:
        response = requests.get(url)
        json_response = response.json()
        return json_response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    api_url = input("Enter the API URL: ")
    data = get_api_data(api_url)
    print("Data from the API:")
    pp(data)
