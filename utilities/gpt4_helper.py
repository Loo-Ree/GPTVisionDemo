import datetime
import openai
import base64
import requests
import json
import copy

def gpt4VWithExtensions(imageenc, query, context, ApiKey, VisionApiKey, ApiBase, VisionApiEndpoint, Gpt4VisionModelDeployment, temperature, gpt4venhancementsapiversion):
    """
    GPT-4 Turbo with vision and Azure AI enhancements
    """
        # Azure Open AI
    openai.api_type: str = "azure"
    openai.api_key = ApiKey
    openai.api_base = ApiBase
    model = Gpt4VisionModelDeployment
    indexname = "car-reports-tests"
    # Azure AI Vision (aka Azure Computer Vision)
    azure_aivision_endpoint = VisionApiEndpoint
    azure_aivision_key = VisionApiKey
    
    
    # Endpoint
    base_url = f"{openai.api_base}openai/deployments/{model}"
    gpt4vision_endpoint = (
        f"{base_url}/extensions/chat/completions?api-version={gpt4venhancementsapiversion}"
    )

    # Header
    headers = {"Content-Type": "application/json", "api-key": openai.api_key}
    
    # Encoded image
    base_64_encoded_image = base64.b64encode(imageenc).decode("ascii")

    # Payload
    json_data = {
        #"model": "gpt-4-vision-deployment",
        "enhancements": {
            "ocr": {
                "enabled": True
            }, 
            "grounding": {
                "enabled": True
            }
        },
        "dataSources": [
            {
                "type": "AzureComputerVision",
                "parameters": { 
                    "endpoint": azure_aivision_endpoint,
                    "key": azure_aivision_key
                }
            }
        ],
        "messages": [
            {
                "role": "system", 
                "content": context
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/jpeg;base64," + base_64_encoded_image
                        }
                    }
                ]
            },
        ],
        "max_tokens": 4000,
        "temperature": temperature,
        "stream": False
        #"top_p": 1,
    }
    
    # Response
    print("DEBUG: sending call to GPT: " + gpt4vision_endpoint)
    
    json_dict = copy.deepcopy(json_data)
    for message in json_dict['messages']:
        if message['role'] == 'user':
            for content in message['content']:
                if content['type'] == 'image_url':
                    # Truncate the image data
                    content['image_url']['url'] = content['image_url']['url'][:100] + '...'
    print("DEBUG: GPT4v full json: " + json.dumps(json_dict))
    
    response = requests.post(
        gpt4vision_endpoint, headers=headers, data=json.dumps(json_data)
    )

    # Testing the status code from the model response
    res = "no response"
    
    if response.status_code == 200:
        now = str(datetime.datetime.today().strftime("%d-%b-%Y %H:%M:%S"))
        result = json.loads(response.text)
        jsn = response.json
        res = result["choices"][0]["message"]["content"]
        print(res)

        print("\n\033[1;31;32mDone:", now)
        
        if "usage" in result: 
            prompt_tokens = result["usage"]["prompt_tokens"]
            completion_tokens = result["usage"]["completion_tokens"]
            total_tokens = result["usage"]["total_tokens"]
            print(f"Prompt tokens = {prompt_tokens} | Completion tokens = {completion_tokens} | Total tokens = {total_tokens}")
        
        return res
    
    elif response.status_code == 429:
        res = f"[429 Error] Too many requests. Please wait a couple of seconds and try again.\n '{json.loads(response.text)}'"
        print(json.loads(response.text))

    else:
        res = f"[Error] Error Code: {response.status_code}\n '{json.loads(response.text)}'"
        print(json.loads(response.text))

    return res
    
def gpt4o(imageenc, query, context, ApiKey, ApiBase, modelDeployment, temperature, apiVersion, ocrText=None):
    """
    GPT-4 Omin with vision and Azure AI enhancements
    """
        # Azure Open AI
    openai.api_type: str = "azure"
    openai.api_key = ApiKey
    openai.api_base = ApiBase
    model = modelDeployment
    
    
    # Endpoint
    base_url = f"{openai.api_base}openai/deployments/{model}"
    gpt4o_endpoint = (
        f"{base_url}/chat/completions?api-version={apiVersion}"
    )

    # Header
    headers = {"Content-Type": "application/json", "api-key": openai.api_key}
    
    # Encoded image
    base_64_encoded_image = base64.b64encode(imageenc).decode("ascii")

    # Payload
    json_data = {
        "messages": [
            {
                "role": "system", 
                "content": context
            },
            {
                "role": "user", 
                "content": [
                    {
                        "type": "text",
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/jpeg;base64," + base_64_encoded_image
                        }
                    }
                ]
            },
        ],
        "max_tokens": 4000,
        "temperature": temperature,
        "stream": False
        #"top_p": 1,
    }
    
    # If ocr_output is provided, add it to the user content
    if ocrText is not None:
        print("DEBUG: OCR text: " + ocrText)
        json_data['messages'][1]['content'].append({
            "type": "text",
            "text": """The following text was extracted by an OCR. Use that text for enhancing your recognition of any text in any provided image.
            Give preference to the OCR text if it is present, but do not ignore the text in the image.
                """ + ocrText
        })
    
    # Response
    print("DEBUG: sending call to GPT: " + gpt4o_endpoint)
    
    json_dict = copy.deepcopy(json_data)
    for message in json_dict['messages']:
        if message['role'] == 'user':
            for content in message['content']:
                if content['type'] == 'image_url':
                    # Truncate the image data
                    content['image_url']['url'] = content['image_url']['url'][:100] + '...'
    print("DEBUG: GPT4o full json: " + json.dumps(json_dict))

    response = requests.post(
        gpt4o_endpoint, headers=headers, data=json.dumps(json_data)
    )

    # Testing the status code from the model response
    res = "no response"
    
    if response.status_code == 200:
        now = str(datetime.datetime.today().strftime("%d-%b-%Y %H:%M:%S"))
        result = json.loads(response.text)
        jsn = response.json
        res = result["choices"][0]["message"]["content"]
        print(res)

        print("\n\033[1;31;32mDone:", now)
        
        if "usage" in result: 
            prompt_tokens = result["usage"]["prompt_tokens"]
            completion_tokens = result["usage"]["completion_tokens"]
            total_tokens = result["usage"]["total_tokens"]
            print(f"Prompt tokens = {prompt_tokens} | Completion tokens = {completion_tokens} | Total tokens = {total_tokens}")
        
        return res
    
    elif response.status_code == 429:
        res = f"[429 Error] Too many requests. Please wait a couple of seconds and try again.\n '{json.loads(response.text)}'"
        print(json.loads(response.text))

    else:
        res = f"[Error] Error Code: {response.status_code}\n '{json.loads(response.text)}'"
        print(json.loads(response.text))

    return res

def gpt4(query, context, apikey, apibase, gptmodel, temperature, gpt4apiversion):
    """
    GPT invoke
    """
    # Azure Open AI
    openai.api_type: str = "azure"
    openai.api_key = apikey
    openai.api_base = apibase
    model = gptmodel
    
    # Endpoint
    base_url = f"{openai.api_base}openai/deployments/{model}"
    endpoint = f"{base_url}/chat/completions?api-version={gpt4apiversion}"

    # Header
    headers = {"Content-Type": "application/json", "api-key": openai.api_key}

    # Context
    context = """
        You are a car mechanic AI expert that support Insurance agent to estimate repairing costs from the description of a damaged car.
        ALWAYS ANSWER IN ITALIAN.
        """

    # Prompt
    data = {
        "messages": [
            {"role": "system", "content": context },
            {"role": "user", "content": query },
        ],
        "max_tokens": 4000,
        "temperature": temperature,
        "stream": False
    }
    

    # Results
    print("DEBUG: sending call to GPT: " + endpoint)
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    
    result = "no response"
    if response.status_code == 200:
        result = json.loads(response.text)["choices"][0]["message"]["content"]
    else:
        if response.status_code == 429:
            result ="[ERROR] Too many requests. Please wait a couple of seconds and try again."
        else:
            result = f"[ERROR] Error code: '{response.status_code}'" 

    return result