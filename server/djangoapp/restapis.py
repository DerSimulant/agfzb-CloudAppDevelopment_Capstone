import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth



# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    response = None  # Declare response here
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url=url, 
            headers={'Content-Type': 'application/json', 'apikey': api_key},
            params=kwargs
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    
    if response:
        status_code = response.status_code
        print("With status {} ".format(status_code))
        
        if status_code == 200:
            # If request was successful, load response data into a JSON format
            json_data = json.loads(response.text)
            return json_data
    
    # If request was not successful or an exception occurred, return an error message
    return {"error": "Request failed or network exception occurred"}



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url="https://eu-de.functions.appdomain.cloud/api/v1/web/5f6babc9-6519-4062-ac30-e2b3b37a1776/dealership-package/get-dealership", api_key="o5POKqlisry_eOetmb67wUNJKxRje-pkVOZ3zeKr34_t")
    if json_result:
        # Get the row list in JSON as dealers
       if 'rows' in json_result:
            # Get the row list in JSON as dealers
            dealers = json_result["rows"]
            # For each dealer object
            for dealer in dealers:
                # Get its content in `doc` object
                dealer_doc = dealer["doc"]
                # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                results.append(dealer_obj)
       else:
            print("'rows' key not found in json_result")

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



