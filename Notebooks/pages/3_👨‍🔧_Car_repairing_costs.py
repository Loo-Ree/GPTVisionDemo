import streamlit as st
import base64
import datetime
import glob
import json
import openai
import os
import requests
import sys

from io import BytesIO
from PIL import Image

import myglobal
from myglobal import AzureKeys

st.set_page_config(
page_title="Stima costi di carrozzeria",
page_icon=":male-mechanic:"
)   

def gpt4V(imageenc, query, ApiKey, VisionApiKey, ApiBase, VisionApiEndpoint, gptModel):
    """
    GPT-4 Turbo with vision and Azure AI enhancements
    """
        # Azure Open AI
    openai.api_type: str = "azure"
    openai.api_key = ApiKey
    openai.api_base = ApiBase
    model = gptModel
    indexname = "car-repairing-tests"
    # Azure AI Vision (aka Azure Computer Vision)
    azure_aivision_endpoint = VisionApiEndpoint
    azure_aivision_key = VisionApiKey
    
    
    # Endpoint
    base_url = f"{openai.api_base}/openai/deployments/{model}"
    gpt4vision_endpoint = (
        f"{base_url}/extensions/chat/completions?api-version=2023-12-01-preview"
    )

    # Header
    headers = {"Content-Type": "application/json", "api-key": openai.api_key}
    
    # Encoded image
    base_64_encoded_image = base64.b64encode(imageenc).decode("ascii")
    
    # Context
    context = """
You are a car mechanic AI expert that support Insurance agent to list car damages from a picture.
Always reply in Italian.
"""
    # Payload
    json_data = {
        "model": "gpt-4-vision-preview",
        "enhancements": {"ocr": {"enabled": True}, "grounding": {"enabled": True}},
        "dataSources": [
            {
                "type": "AzureComputerVision",
                "endpoint": azure_aivision_endpoint,
                "key": azure_aivision_key,
                "indexName": indexname,
            }
        ],
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": [query, {"image": base_64_encoded_image}]},
        ],
        "max_tokens": 4000,
        "temperature": 0.7,
        "top_p": 1,
    }
    
    # Response
    print("DEBUG: invio dati a GPT4V")
    print(gpt4vision_endpoint)
    response = requests.post(
        gpt4vision_endpoint, headers=headers, data=json.dumps(json_data)
    )

    # Testing the status code from the model response
    res = "no response"
    
    if response.status_code == 200:
        now = str(datetime.datetime.today().strftime("%d-%b-%Y %H:%M:%S"))
        result = json.loads(response.text)
        res = result["choices"][0]["message"]["content"]
        print(res)
        
        prompt_tokens = result["usage"]["prompt_tokens"]
        completion_tokens = result["usage"]["completion_tokens"]
        total_tokens = result["usage"]["total_tokens"]

        print("\n\033[1;31;32mDone:", now)
        print(f"Prompt tokens = {prompt_tokens} | Completion tokens = {completion_tokens} \
| Total tokens = {total_tokens}")
        
        return res
    
    elif response.status_code == 429:
        res = f"[429 Error] Too many requests. Please wait a couple of seconds and try again.\n '{json.loads(response.text)}'"
        print(json.loads(response.text))

    else:
        res = f"[Error] Error Code: {response.status_code}\n '{json.loads(response.text)}'"
        print(json.loads(response.text))

    return res

def GPTcall(query, apikey, apibase, gptmodel):
    """
    GPT invoke
    """
    # Azure Open AI
    openai.api_type: str = "azure"
    openai.api_key = apikey
    openai.api_base = apibase
    model = gptmodel
    
    # Endpoint
    base_url = f"{openai.api_base}/openai/deployments/{model}"
    endpoint = f"{base_url}/chat/completions?api-version=2023-12-01-preview"

    # Header
    headers = {"Content-Type": "application/json", "api-key": openai.api_key}

    # Context
    context = """
        You are a car mechanic AI expert that support Insurance agent to estimate repairing costs from the description of a damaged car.
        Always reply in Italian.
        """

    # Prompt
    data = {
        "messages": [
            {"role": "system", "content": context },
            {"role": "user", "content": query },
        ],
        "max_tokens": 4000,
    }
    

    # Results
    print("DEBUG: invio dati a GPT4V")
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

def main():
    if st.session_state['authentication_status']:
        st.title("GPT4-Vision demo - Stima costi di carrozzeria")
        
        # Carica l'immagine
        imagelink = st.file_uploader("Carica la foto di una automobile incidentata", type=["jpg", "jpeg", "png"])
        if imagelink is not None:
            st.image(imagelink, caption=imagelink.name, use_column_width=True)
        
        #costi di riparazione
        prezzi = st.text_area("Costi di riparazione", height=200, value="""
        - cofano nuovo: 40000€-50000€
        - paraurti nuovo: 25000€-30000€
        - griglia nuova: 5000€-8000€
        - fari nuovi: 6000€-9000€
        - airbag nuovo: 1000€-3000€
        - costo orario di manodopera: 500€/ora
                """)
        
        # Elabora l'immagine con un prompt fisso quando viene premuto il pulsante
        if st.button("Stima Costi Carrozzeria"):
            if imagelink is not None and prezzi != "":
                message = st.success("Analisi in corso...")
                #analisi della foto
                prompt = "descrivi in dettaglio i danni a questa automobile"
                resDescription = gpt4V(imagelink.read(), prompt, AzureKeys.ApiKey, AzureKeys.VisionApiKey, AzureKeys.ApiBase, AzureKeys.VisionApiEndpoint, AzureKeys.GptModel)
                message.empty()
                st.success(resDescription)                
                #analisi dei danni
                prompt = f"""
                Classifica i tipi di danni riscontrati nell'automobile descritti di seguito in modo da stimarne i costi di riparazione. 
                Ipotizza anche le ore di lavoro necessarie per ogni riparazione o sostituzione e calcolane il costo considerando i costi seguenti.
                Considera i range di costo seguenti per la valutazione o ipotizzali se non presenti in questa lista:
                {prezzi}
                """
                query = f"{prompt}:\n'{resDescription}'"
                message = st.success("Stima costi in corso...")
                result = GPTcall(query, AzureKeys.ChatApiKey, AzureKeys.ChatApiBase, AzureKeys.ChatGptModel)
                message.empty()
                st.success(result)
            else:
                st.warning("Per favore, carica un'immagine di una auto incidentata.")
    
        #immagini di esempio
        samplec = st.expander("Samples", expanded=False)
        with samplec:
            col1, col2 =  st.columns(2)
            #Sample1
            with col1:
                sample1 = "./app/static/incidente1.jpg"
                st.markdown(
                    f'<a href="{sample1}" target="_blank" download ><img src="{sample1}" height="100"></a>',
                    unsafe_allow_html=True,
                )
            # #Sample2
            # with col2:
            #     sample2 = "./app/static/car_report2.jpg"
            #     st.markdown(
            #         f'<a href="{sample2}" target="_blank" download ><img src="{sample2}" height="100"></a>',
            #         unsafe_allow_html=True,
            #     )
            
    #st.info("© 2023 - GPT4-Vision - Microsoft Azure OpenAI - Demo")
    else:
        st.error("...credo serva una password... ⛔")
        
if __name__ == "__main__":
    main()
