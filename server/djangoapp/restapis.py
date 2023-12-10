import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = "_oY17kD5rUZN_rjp2nwgrvTwrc1Eepjf8uIq1IkHXM1a"
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    api_key = "_oY17kD5rUZN_rjp2nwgrvTwrc1Eepjf8uIq1IkHXM1a"
    # try:
    response = requests.post(url, headers={'Content-Type': 'application/json'},
        auth=HTTPBasicAuth('apikey', api_key), json = json_payload,
        params=kwargs
    )
    # except:
    #     print("Network exception occured")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], state=dealer_doc["state"],
                                    full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url+"?id="+str(dealerId))
    if json_result:
        reviews = json_result
        for review in reviews:
            reviews_doc = review
            review_obj = DealerReview(car_make=reviews_doc["car_make"], car_model=reviews_doc["car_model"], car_year=reviews_doc["car_year"],
                                    dealership=reviews_doc["dealership"],
                                    id=reviews_doc["id"], name=reviews_doc["name"], purchase=reviews_doc["purchase"],
                                    purchase_date=reviews_doc["purchase_date"],
                                    review=reviews_doc["review"], sentiment="")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

def get_dealer_by_id_from_cf(url, dealerId):
    json_result = get_request(url+"?id="+str(dealerId))
    if json_result:
        dealer = json_result[0]
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], state=dealer["state"],
                                full_name=dealer["full_name"],
                                id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                short_name=dealer["short_name"],
                                st=dealer["st"], zip=dealer["zip"])
        return dealer_obj
    return None

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/b8dba7e0-bd27-41c4-b15a-242ebed8f20d/v1/analyze?version=2019-07-12"
    api_key = "_oY17kD5rUZN_rjp2nwgrvTwrc1Eepjf8uIq1IkHXM1a"
    headers = {"Content-Type": "application/json"}
    req_body = {
        "text": dealerreview,
        "features": {
            "sentiment": {
                "document": True
            }
        }
    }
    json_req = json.dumps(req_body)
    print(json_req)
    response = requests.post(url, json=req_body, headers=headers, auth=HTTPBasicAuth('apikey', api_key))
    print(str(response.status_code)+" "+response.text)
    if response.status_code != 200:
        return ""
    json_data = json.loads(response.text)
    return json_data["sentiment"]["document"]["label"]  