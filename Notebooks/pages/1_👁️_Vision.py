import streamlit as st
import datetime
import openai
import os
import base64
import requests
import json
import sys
import myglobal
from myglobal import AzureKeys

from openai import AzureOpenAI
from IPython.display import Image

st.set_page_config(
page_title="GPT4-Vision demo",
page_icon=":eye:"
)

def gpt4V(imageenc, query, apikey, apibase, gptmodel):
    """
    GPT4-Vision
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

    base_64_encoded_image = base64.b64encode(imageenc).decode("ascii")
    
    # Prompt
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Always answer in italian."},
            {"role": "user", "content": [query, {"image": base_64_encoded_image}]},
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

def gpt4Vplus(imageenc, query, ApiKey, VisionApiKey, ApiBase, VisionApiEndpoint, gptModel):
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
You are a helpful assistant. Always answer in italian.
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
        st.title("GPT4-Vision demo")
        
        # Carica l'immagine
        imagelink = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png"])
        if imagelink is not None:
            st.image(imagelink, caption=imagelink.name, use_column_width=True)
        
        # Inserisci il testo
        text = st.text_input("Inserisci un testo", "What is it?")
        
        # Elabora l'immagine e il testo quando viene premuto il pulsante
        if st.button("Elabora"):
            if imagelink is not None and text != "":
                message = st.success("Elaborazione in corso...")
                result = gpt4Vplus(imagelink.read(), text, AzureKeys.ApiKey, AzureKeys.VisionApiKey, AzureKeys.ApiBase, AzureKeys.VisionApiEndpoint, AzureKeys.GptModel)
                message.empty()
                st.success(result)
            else:
                st.warning("Per favore, carica un'immagine e inserisci una domanda.")
        
        #immagini di esempio
        samplec = st.expander("Samples", expanded=False)
        with samplec:
            col1, col2, col3, col4 =  st.columns(4)
            #Sample1
            with col1:
                sample1 = "./app/static/amazon-lego.png"
                st.markdown(
                    f'<a href="{sample1}" target="_blank" download="Amazon" ><img src="{sample1}" height="100"></a>',
                    unsafe_allow_html=True,
                )
                sample5 = "./app/static/matrimonio.jpeg"
                st.markdown(
                    f'<a href="{sample5}" target="_blank" download="attoMatrimonio" ><img src="{sample5}" height="100"></a>',
                    unsafe_allow_html=True,
                )
            #Sample2
            with col2:
                sample2 = "./app/static/foca.jpg"
                st.markdown(
                    f'<a href="{sample2}" target="_blank" download="focaDivertente" ><img src="{sample2}" height="100"></a>',
                    unsafe_allow_html=True,
                )
                sample6 = "./app/static/nolan_collection.jpg"
                st.markdown(
                    f'<a href="{sample6}" target="_blank" download="DVDbox" ><img src="{sample6}" height="100"></a>',
                    unsafe_allow_html=True,
                )
            #Sample3
            with col3:
                sample3 = "./app/static/funny.png"
                st.markdown(
                    f'<a href="{sample3}" target="_blank" download="funnyMeme" ><img src="{sample3}" height="100"></a>',
                    unsafe_allow_html=True,
                )
                sample7 = "./app/static/ricetta1.jpeg"
                st.markdown(
                    f'<a href="{sample7}" target="_blank" download="ricettaMedica" ><img src="{sample7}" height="100"></a>',
                    unsafe_allow_html=True,
                )                
            #Sample3
            with col4:
                sample4 = "./app/static/giulia.jpeg"
                st.markdown(
                    f'<a href="{sample4}" target="_blank" download ><img src="{sample4}" height="100"></a>',
                    unsafe_allow_html=True,
                )
            
        st.info("© 2023 - GPT4-Vision - Microsoft Azure OpenAI - Demo")
    else:
        st.error("...credo serva una password... ⛔")

if __name__ == "__main__":
    main()
