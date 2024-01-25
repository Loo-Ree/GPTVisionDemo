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
page_title="Gestione Convenzione Indennizzo Diretto (CID)",
page_icon=":blue_car:"
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
    indexname = "car-reports-tests"
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
You are an insurance AI expert. You will analyse a car report document. 
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

def main():
    if st.session_state['authentication_status']:
        st.title("GPT4-Vision demo - Gestione Convenzione Indennizzo Diretto (CID)")
        
        # Carica l'immagine
        imagelink = st.file_uploader("Carica un modulo CID", type=["jpg", "jpeg", "png"])
        if imagelink is not None:
            st.image(imagelink, caption=imagelink.name, use_column_width=True)
        
        # Inserisci il testo
        option = st.selectbox("Scegli una domanda", 
                    ["Generate a summary", "Do we have some witness?", "Explain the drawing from section number 13", "How many signatures do we have at the end of the document?", "What are the damages for vehicles A and B?"
                        ])
        text = st.text_input("o digitane una", option)        
        
        # Elabora l'immagine e con la query utente quando viene premuto il pulsante
        if st.button("Query"):
            if imagelink is not None and text != "":
                message = st.success("Elaborazione in corso...")
                result = gpt4V(imagelink.read(), text, AzureKeys.ApiKey, AzureKeys.VisionApiKey, AzureKeys.ApiBase, AzureKeys.VisionApiEndpoint, AzureKeys.GptModel)
                message.empty()
                st.success(result)
            else:
                st.warning("Per favore, carica un'immagine e inserisci una domanda.")
                
        # Elabora l'immagine con un prompt fisso quando viene premuto il pulsante
        if st.button("CID Analyzer"):
            if imagelink is not None and text != "":
                message = st.success("Analisi in corso...")
                prompt = """
    You respond in Italian with your analysis of the following fields:

    1. Summary: Create a summary of this car report.
    2. Names: What are the names of owners of vehicle A and B? \
    Just answer like vehicle A = 'SMITH', Vehicle B = 'JOHNSON'
    3. Vehicles: What is the brand and model of vehicle A and B? \
    Just answer like vehicle A = 'AUDI', Vehicle B = 'MERCEDES'
    4. Date and time: What is the date and time of the accident? \
    Just answer like '01-jan-2023 22:00'
    5. Address: What is the address of the accident? \
    Just answer like '78 Avenue de Paris 75012 Paris'
    6. Damage: Share some information about the damage.
    Others damage: Display some information about material damage other than to vehicles A and B.
    7. Injured people: Do we have injured people?
    8. Section 14 comments: What are the comments in section 14?
    9. Damage classification: Classify this damage as LIGHT DAMAGE, MEDIUM DAMAGE, SEVERE DAMAGE.
    10. Drawings #10: Explain the drawings from section number 10 for vehicles A and B?
    11. Drawing #13: Explain the drawing from section number 13?
    12. Signatures: Do we have two signatures at the end of this document? \
    Just answer like "Two signatures detected", "One signature detected", "No signature detected"
    """
                result = gpt4V(imagelink.read(), prompt, AzureKeys.ApiKey, AzureKeys.VisionApiKey, AzureKeys.ApiBase, AzureKeys.VisionApiEndpoint, AzureKeys.GptModel)
                message.empty()
                st.success(result)
            else:
                st.warning("Per favore, carica un'immagine CID.")
    
        #immagini di esempio
        samplec = st.expander("Samples", expanded=False)
        with samplec:
            col1, col2 =  st.columns(2)
            #Sample1
            with col1:
                sample1 = "./app/static/car_report1.jpg"
                st.markdown(
                    f'<a href="{sample1}" target="_blank" download ><img src="{sample1}" height="100"></a>',
                    unsafe_allow_html=True,
                )
            #Sample2
            with col2:
                sample2 = "./app/static/car_report2.jpg"
                st.markdown(
                    f'<a href="{sample2}" target="_blank" download ><img src="{sample2}" height="100"></a>',
                    unsafe_allow_html=True,
                )
            
    #st.info("© 2023 - GPT4-Vision - Microsoft Azure OpenAI - Demo")
    else:
        st.error("...credo serva una password... ⛔")
        
if __name__ == "__main__":
    main()
