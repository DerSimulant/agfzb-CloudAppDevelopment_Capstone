import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth



# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None,**kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    response = None  # Declare response here
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            # Basic authentication GET
            response = requests.get(
                url,
                params=kwargs,
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', api_key)
            )
        else:
            # No authentication GET
            response = requests.get(
                url,
                params=kwargs,
                headers={'Content-Type': 'application/json'}
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
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    response = None  
    try:
        response = requests.post(
            url=url, 
            headers={'Content-Type': 'application/json'},
            params=kwargs,
            json=json_payload
        )
    except:
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = response.json()

    return json_data



# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the dealership list in JSON
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer_doc in dealers:
            # Create a CarDealer object with values in dealer_doc object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, dealerId, **kwargs):
    results = []
    # Call get_request with a URL parameter and dealerId
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the dealership list in JSON
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer_doc in dealers:
            # If the dealer's id matches the search id
            if dealer_doc["id"] == dealerId:
                # Create a CarDealer object with values in dealer_doc object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
                results.append(dealer_obj)
    return results

def get_dealers_by_state(url, state, **kwargs):
    results = []
    # Call get_request with a URL parameter and state
    json_result = get_request(url, state=state)
    if json_result:
        # Get the dealership list in JSON
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer_doc in dealers:
            # If the dealer's state matches the search state
            if dealer_doc["state"].lower() == state.lower():
                # Create a CarDealer object with values in dealer_doc object
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
                results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id, api_key):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        reviews = json_result["reviews"]
        for review_doc in reviews:
            # Analyze sentiment with Watson NLU
            #sentiment = analyze_review_sentiments(review_doc["review"], api_key)
            
            # Use get to avoid KeyError if purchase, id or name fields are missing
            purchase = review_doc.get("purchase", False)
            id_value = review_doc.get("id", None)
            name = review_doc.get("name", "")
            
            # Get the purchase_date, car_make, car_model, and car_year only if purchase is True
            purchase_date = review_doc.get("purchase_date") if purchase else None
            car_make = review_doc.get("car_make") if purchase else None
            car_model = review_doc.get("car_model") if purchase else None
            car_year = review_doc.get("car_year") if purchase else None
            
            review_obj = DealerReview(dealership=review_doc["dealership"],
                                      name=name,
                                      purchase=purchase,
                                      review=review_doc["review"],
                                      purchase_date=purchase_date,
                                      car_make=car_make,
                                      car_model=car_model,
                                      car_year=car_year,
                                      #sentiment=sentiment,
                                      id=id_value)
            results.append(review_obj)
    return results








# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
def analyze_review_sentiments(review, api_key):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/194721c1-b3d0-4a7f-9ff9-17dd89bcf03a"
    params = {
        "text": review,
        "version": "2021-03-25",
        "features": "sentiment",
        "return_analyzed_text": True
    }
    response = get_request(url, api_key=api_key, **params)
    print(response)

    sentiment = None
    sentiment = response["sentiment"]["document"]["label"]
    if "sentiment" in response:
        if "document" in response["sentiment"]:
            sentiment = response["sentiment"]["document"]["label"]

    # Rückgabe des Sentiments
    return sentiment
    
    



