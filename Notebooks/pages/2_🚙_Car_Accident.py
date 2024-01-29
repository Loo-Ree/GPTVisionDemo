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
page_title="Gestione Convenzione Indennizzo Diretto (CAI)",
page_icon=":blue_car:"
)   

def gpt4V(imageenc, query, ApiKey, VisionApiKey, ApiBase, VisionApiEndpoint, Gpt4VisionModel):
    """
    GPT-4 Turbo with vision and Azure AI enhancements
    """
        # Azure Open AI
    openai.api_type: str = "azure"
    openai.api_key = ApiKey
    openai.api_base = ApiBase
    model = Gpt4VisionModel
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
        st.title("GPT4-Vision demo - Gestione Convenzione Indennizzo Diretto (CAI)")
        
        # Carica l'immagine
        imagelink = st.file_uploader("Carica un modulo CAI", type=["jpg", "jpeg", "png"])
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
                result = gpt4V(imagelink.read(), text, AzureKeys.ApiKey, AzureKeys.VisionApiKey, AzureKeys.ApiBase, AzureKeys.VisionApiEndpoint, AzureKeys.Gpt4VisionModel)
                message.empty()
                st.success(result)
            else:
                st.warning("Per favore, carica un'immagine e inserisci una domanda.")
                
        #prompt config
        promptconfig = st.expander("Prompt Config", expanded=False)
        with promptconfig:
                    CAIPrompt = st.text_area("CAI Prompt", """
                Rispondi in italiano con la tua analisi dei seguenti campi:

                1. Sommario: Crea un sommario di questa Constatazione Amichevole di Incidente (CAI).
                2. Nomi: Quali sono i nomi dei proprietari dei veicoli A e B? \
                Rispondi semplicemente, ad esempio: veicolo A = 'JOHN SMITH', Veicolo B = 'MIKE JOHNSON'
                3. Veicoli: Qual è la marca e il modello del veicolo A e B? \
                Rispondi semplicemente, ad esempio: veicolo A = 'AUDI', Veicolo B = 'MERCEDES'
                4. Data e ora: Qual è la data e l'ora dell'incidente? \
                Rispondi semplicemente, ad esempio:  '01-gen-2023 22:00'
                5. Indirizzo: Qual è l'indirizzo dell'incidente? \
                Rispondi semplicemente, ad esempio:  '78 Avenue de Paris 75012 Paris'
                6. Danni: Condividi alcune informazioni sui danni.
                Altri danni: Mostra alcune informazioni sui danni materiali diversi dai veicoli A e B se presenti nel documento.
                7. Persone ferite: Abbiamo persone ferite?
                8. Commenti sezione 14: Quali sono i commenti nella sezione 14?
                9. Classificazione dei danni: Classifica questi danni come DANNO LIEVE, DANNO MEDIO, DANNO GRAVE.
                10. Disegni #10: Spiega i disegni della sezione numero 10 per i veicoli A e B.
                Rispondi semplicemente, ad esempio: veicolo A = 'Automobile, danno al faro anteriore sinistro e fiancata anteriore sinistra', Veicolo B = 'Motociclo, danno alla parte anteriore, danno al fianco destro' 
                11. Disegno #13: Spiega il disegno della sezione numero 13.
                Rispondi semplicemente, ad esempio: 'Il veicolo A procedeva su una strada rettilinea mentre il veicolo B sopraggiungeva superandolo. Un contatto si è verificato tra i due veicoli'
                12. Firme: Abbiamo due firme alla fine di questo documento? \
                Rispondi semplicemente come "Due firme rilevate", "Una firma rilevata", "Nessuna firma rilevata"
                """, height=600)
        
        # Elabora l'immagine con un prompt fisso quando viene premuto il pulsante
        if st.button("CAI Analyzer"):
            if imagelink is not None and text != "":
                message = st.success("Analisi in corso...")
                prompt = CAIPrompt
                result = gpt4V(imagelink.read(), prompt, AzureKeys.ApiKey, AzureKeys.VisionApiKey, AzureKeys.ApiBase, AzureKeys.VisionApiEndpoint, AzureKeys.Gpt4VisionModel)
                message.empty()
                st.success(result)
            else:
                st.warning("Per favore, carica un'immagine CAI.")
            
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
            
        st.info("© 2024 - GPT4-Vision - Microsoft Azure OpenAI - Demo")
    else:
        st.error("...credo serva una password... ⛔")
        
if __name__ == "__main__":
    main()
