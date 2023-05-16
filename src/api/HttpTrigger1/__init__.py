import logging
import json
import datetime
from typing import Optional
import uuid
import jwt
import requests
from azure.identity import ClientSecretCredential
from azure.functions import HttpRequest, HttpResponse
from azure.identity import DefaultAzureCredential


import azure.functions as func

# Define  Azure subscription ID, resource group name, and API Management service name
subscriptionId = "2e926ce6-8aad-455c-b48b-7203d9a34b27"
resourceGroupName = "apim-custom-portal"
serviceName = "custom-portal"


credential = DefaultAzureCredential()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    auth_header = req.headers.get('Authorization')
    userid = verify_user(auth_header)
    print(auth_header)
    if userid == "invalid":
        return func.HttpResponse(
            "Token was passed but is invalid",
            status_code=400
        )

    # Parse the route
    route = req.route_params.get('route', '')

    if req.method == "POST" and route == "create_apim_product":
        return create_apim_product(req)
    
    if req.method == "POST" and route == "list_tags":
        return list_tags(req)
    
    if req.method == "GET" and route == "list_apis_of_tagged_products":
        tagIds = req.params.get('tagIds')
        if tagIds is None:
            return func.HttpResponse(
                "Please pass a list of tagIds on the query string or in the request body",
                status_code=400
            )
        else:
            return list_apis_of_tagged_products(tagIds)
    
    if req.method == "GET" and route == "list_apis_of_products":
        productIds = req.params.get('productIds')
        if productIds is None:
            return func.HttpResponse(
                "Please pass a list of productIds on the query string or in the request body",
                status_code=400
            )
        else:
            return list_apis_of_products(productIds)

    if req.method == "GET" and route == "list_tagged_products":
        tagIds = req.params.get('tagIds')
        if tagIds is None:
            return func.HttpResponse(
                "Please pass a list of tagIds on the query string or in the request body",
                status_code=400
            )
        else:
            return list_tagged_products(tagIds)
        

    if req.method == "GET" and route == "list_user_products":
        return list_user_products(userid)
        
    if req.method == "DELETE" and route == "delete_product":
        print("delete_product")
        productId = req.params.get('productId')
        if productId is None:
            return func.HttpResponse(
                "Please pass a list of productIds on the query string or in the request body",
                status_code=400
            )
        else:
            return delete_product(productId,userid)
        
    if req.method == "POST" and route == "create_product":
        productId = req.params.get('productId')
        productApis = req.params.get('productApis')


        if productApis is None:
            return func.HttpResponse(
                "Please pass a list of productApis on the query string or in the request body example: /subscriptions/2e926ce6-8aad-455c-b48b-7203d9a34b27/resourceGroups/apim-custom-portal/providers/Microsoft.ApiManagement/service/custom-portal/products/testbaseproduct1/apis/testapi1",
                status_code=400
            )
        else:
            return create_or_update_product(productId, productApis, userid)

    if req.method == "POST" and route == "check_and_create_tag":
        tagId = req.params.get('tagId')
        if tagId is None:
            return func.HttpResponse(
                "Please pass a tagId on the query string or in the request body",
                status_code=400
            )
        else:
            return check_and_create_tag(tagId)

    return HttpResponse(
        json.dumps({"error": "Invalid request"}),
        status_code=400
    )


def get_token():
    # Get access token
    token = credential.get_token('https://management.azure.com/.default')
    print(token.token)
    return token.token

def verify_user(auth_header):

    headers = {
        "Authorization": auth_header
    }

    print(headers)
    endpoint = f"https://custom-portal.management.azure-api.net/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/identity?api-version=2022-08-01"
    response = requests.get(endpoint, headers=headers)

    print(response.status_code)
    print(endpoint)

    if response.status_code != 200:
        return "invalid"
    elif response.status_code == 200:
        id_value = response.json().get('id')
        return id_value

def create_headers():
    token = get_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    return headers

def check_and_create_tag(tagId: str) -> HttpResponse:
    # Define  API Management REST endpoint
    apim_endpoint = f'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/tags/{tagId}?api-version=2019-12-01'

    headers = create_headers()

    # First, check if the tag exists by sending a GET request
    response = requests.get(apim_endpoint, headers=headers)

    # If the tag does not exist, the response status code will be 404
    if response.status_code == 404:
        print("Tag does not exist. Creating tag...")
        # Define  request body for creating a new tag
        body = {
            "properties": {
                "displayName": tagId
            }
        }

        # Create the tag by sending a PUT request
        response = requests.put(apim_endpoint, headers=headers, json=body)

    # Return the response
    if response.status_code in [200, 201]:  # 200 for successful GET, 201 for successful PUT
        return HttpResponse(
            json.dumps(response.json()),
            headers={"Content-Type": "application/json"}
        )
    else:
        return HttpResponse(
            json.dumps({"error": response.text}),
            status_code=400
        )


def list_tags(req: HttpRequest) -> HttpResponse:
    # list all existing tags in APIM
    # Define  API Management REST endpoint
    apim_endpoint = f'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/tags?api-version=2019-12-01'

    # Make the GET request
    headers = create_headers()
    response = requests.get(apim_endpoint, headers=headers)

    if response.status_code == 200:
        return HttpResponse(
            json.dumps(response.json()),
            headers={"Content-Type": "application/json"}
        )
    else:
        return HttpResponse(
            json.dumps({"error": response.text}),
            status_code=400
        )

def create_apim_product(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    headers = create_headers()

    # Define  API Management REST endpoint
    apim_endpoint = 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}?api-version=2019-12-01'

    # Define  request body
    body = {
        "properties": {
            # Fill in  properties here
        }
    }

    # Make the POST request
    response = requests.post(apim_endpoint, headers=headers, json=body)
    
    if response.status_code == 200:
        return HttpResponse(
            json.dumps(response.json()),
            headers={"Content-Type": "application/json"}
        )
    else:
        return HttpResponse(
            json.dumps({"error": response.text}),
            status_code=400
        )
    
def list_apis_of_tagged_products(tagIds: list) -> HttpResponse:
    headers = create_headers()
    all_apis = []
    tagIds = tagIds.split(',')
    for tagId in tagIds:
        # Define  API Management REST endpoint for getting the tag
        tag_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/tagResources?$filter=tag/name eq '{tagId}' &api-version=2022-08-01"
    
        # Send a GET request to retrieve the tag
        tag_response = requests.get(tag_endpoint, headers=headers)
        if tag_response.status_code != 200:
            return HttpResponse(
                json.dumps({"error": tag_response.text}),
                status_code=400
            )
        
        # Assuming each item in the 'value' list contains a 'product' field with 'id' as the productId
        productIds = [item.get('product', {}).get('id') for item in tag_response.json().get('value', [])]
        print("productIds")
        print(productIds)
        if not productIds:
            return HttpResponse(
                json.dumps({"error": f"No product associated with the given tag {tagId}"}),
                status_code=400
            )
        
        for productId in productIds:
            apis_endpoint = f'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}{productId}/apis?api-version=2022-08-01'
            print("apis_endpoint")
            print(apis_endpoint)
            apis_response = requests.get(apis_endpoint, headers=headers)

            if apis_response.status_code == 200:
                all_apis.extend(apis_response.json().get('value', []))
            else:
                return HttpResponse(
                    json.dumps({"error": apis_response.text}),
                    status_code=400
                )

    return HttpResponse(
        json.dumps(all_apis),
        headers={"Content-Type": "application/json"}
    )

def list_tagged_products(tagIds: str) -> HttpResponse:
    headers = create_headers()
    all_products = []
    tagIds = tagIds.split(',')


    print(tagIds)
    
    for tagId in tagIds:
        # Define  API Management REST endpoint for getting the tag
        tag_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/tagResources?$filter=tag/name eq '{tagId}' &api-version=2022-08-01"
    
        # Send a GET request to retrieve the tag
        tag_response = requests.get(tag_endpoint, headers=headers)
        if tag_response.status_code != 200:
            return HttpResponse(
                json.dumps({"error": tag_response.text}),
                status_code=400
            )
        
        # Assuming each item in the 'value' list contains a 'product' field with all the product details
        products = [item.get('product', {}) for item in tag_response.json().get('value', [])]

        if products:
            all_products.extend(products)


    return HttpResponse(
        json.dumps(all_products),
        headers={"Content-Type": "application/json"}
    )

def list_user_products(userid: str) -> HttpResponse:
    headers = create_headers()
    all_products = []
    tagIds = []
    tagIds.append(userid)

    print(tagIds)
    
    for tagId in tagIds:
        # Define  API Management REST endpoint for getting the tag
        tag_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/tagResources?$filter=tag/name eq '{tagId}' &api-version=2022-08-01"
    
        # Send a GET request to retrieve the tag
        tag_response = requests.get(tag_endpoint, headers=headers)
        if tag_response.status_code != 200:
            return HttpResponse(
                json.dumps({"error": tag_response.text}),
                status_code=400
            )
        
        # Assuming each item in the 'value' list contains a 'product' field with all the product details
        products = [item.get('product', {}) for item in tag_response.json().get('value', [])]

        if products:
            all_products.extend(products)


    return HttpResponse(
        json.dumps(all_products),
        headers={"Content-Type": "application/json"}
    )

def list_apis_of_products(productIds: str) -> HttpResponse:
    headers = create_headers()
    all_apis = []
    productIds = productIds.split(',')

    for productId in productIds:
        # Define  API Management REST endpoint for listing APIs of the product
        apis_endpoint = f'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}{productId}/apis?api-version=2022-08-01'

        # Send a GET request to retrieve the APIs
        apis_response = requests.get(apis_endpoint, headers=headers)

        if apis_response.status_code != 200:
            return HttpResponse(
                json.dumps({"error": apis_response.text}),
                status_code=400
            )

        # Assuming the APIs are in the 'value' field of the response
        all_apis.extend(apis_response.json().get('value', []))

    return HttpResponse(
        json.dumps(all_apis),
        headers={"Content-Type": "application/json"}
    )

def create_or_update_product(productId: Optional[str], productApis: str, userid: str) -> HttpResponse:
    headers = create_headers()

    # Hardcoded tag
    tagId = userid
    
    # Check and create the tag if it doesn't exist
    tag_response = check_and_create_tag(tagId)
    if tag_response.status_code != 200:
        return HttpResponse(
            json.dumps({"error": tag_response.text}),
            status_code=400
        )
    
    if productId is None:
        # If productId is not provided, generate a random productId for the new product
        productId = f"product-{str(uuid.uuid4())[:5]}"



    # Define the endpoint for creating or updating the product
    product_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/products/{productId}?api-version=2022-08-01"

    # Send a PUT request to create or update the product
    body = {
        "properties": {
            "displayName": productId,
            "description": "This is a new product.",
            "terms": "Terms for the new product.",
            "subscriptionRequired": True,
            "approvalRequired": False,
            "subscriptionsLimit": 10,
            "state": "published"
        }
    }

    # Create or update the product by sending a PUT request
    product_response = requests.put(product_endpoint, headers=headers, json=body)

    if product_response.status_code not in [200, 201]:  # 200 for successful GET, 201 for successful PUT
        return HttpResponse(
            json.dumps({"error": product_response.text}),
            status_code=400,
            headers={"Content-Type": "application/json"}
        )

    # Split the comma-separated list of API IDs into individual IDs
    apiIds = productApis.split(',')

    # For each API ID, define the endpoint for adding the API to the product and send a PUT request
    for apiId in apiIds:

        apiId = apiId.rsplit('/', 1)[-1]
        
        api_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/products/{productId}/apis/{apiId}?api-version=2022-08-01"
        api_response = requests.put(api_endpoint, headers=headers)

        if api_response.status_code not in [200, 201]:  # 200 for successful GET, 201 for successful PUT
            return HttpResponse(
                json.dumps({"error": api_response.text}),
                status_code=400,
                headers={"Content-Type": "application/json"}
            )

    # Define the endpoint for adding the tag to the product and send a PUT request
    tag_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/products/{productId}/tags/{tagId}?api-version=2022-08-01"
    tag_response = requests.put(tag_endpoint, headers=headers)

    if tag_response.status_code not in [200, 201]:  # 200 for successful GET, 201 for successful PUT
        return HttpResponse(
            json.dumps({"error": tag_response.text}),
            status_code=400,
            headers={"Content-Type": "application/json"}
        )

    return HttpResponse(
        json.dumps({"success": f"Product {productId} has been created or updated, APIs have been added, and it has been tagged with {tagId}."}),
        headers={"Content-Type": "application/json"}
    )

def delete_product(productId: str, userid: str) -> HttpResponse:
    headers = create_headers()



    # Define the endpoint for deleting the product
    product_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}{productId}?api-version=2022-08-01&deleteSubscriptions=true"

    # Send a DELETE request to remove the product
    response = requests.delete(product_endpoint, headers=headers)
    print("lol1")
    # If the product was successfully deleted, the response status code will be 200
    if response.status_code == 200:
        return HttpResponse(
            json.dumps({"success": f"Product {productId} has been deleted."}),
            headers={"Content-Type": "application/json"}
        )
    else:
        return HttpResponse(
            json.dumps({"error": "Product could not be deleted. It doesn't exist or there was an error."}),
            status_code=400,
            headers={"Content-Type": "application/json"}
        )