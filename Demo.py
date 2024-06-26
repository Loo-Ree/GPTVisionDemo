import os
from dotenv import load_dotenv
import streamlit as st

import myglobal
from myglobal import AzureKeys

st.set_page_config(
    page_title="Microsoft Azure Demos",
    # page_icon="👋",
    page_icon=":robot_face:"
)

def load_env_variables(filename):
    variables = {}
    with open(filename, 'r') as f:
        for line in f:
            name, value = line.strip().split('=')
            variables[name] = value
    return variables

#AUTHN
name, authentication_status, username = myglobal.authenticate('main')

if authentication_status:
    # st.write(f'Welcome *{name}*')
    st.session_state['authentication_status'] = True

    st.write("# Benvenuti nel futuro! 👋")

    st.sidebar.success("Seleziona una demo.")

    st.markdown(
        """
        Azure OpenAI GPT è un modello di apprendimento automatico avanzato sviluppato da OpenAI e Microsoft, utilizzabile da chiunque mediante Azure, la piattaforma cloud di Microsoft. 
        \n GPT significa "Generative Pretrained Transformer", un tipo di modello di intelligenza artificiale che utilizza il machine learning per comprendere e generare linguaggio umano.
        \n
        \n Questo modello è in grado di capire il contesto di un'intera conversazione e di rispondere in modo appropriato, rendendolo utile per una vasta gamma di applicazioni, come chatbot, assistenti virtuali, traduzione automatica, generazione di testo e altro ancora. 
        \n
    """
    )
    
    st.markdown(
    """
    ### 👈 Seleziona una demo qui 
    per vedere qualche esempio di cosa può fare Microsoft Azure e la Generative AI! \n
    - 👁️ Vision - Chiedi a GPT4-Vision e Azure AI Vision di analizzare una immagine
    - 🚙 Car Accident - Carica un modulo di Convenzione Indennizzo Diretto (CAI) relativo ad un incidente e chiedi a GPT4-Vision di analizzarlo
    - 👨‍🔧 Car Repairing Costs - Valuta e stima i costi di riparazione di un'automobile incidentata
    - 🤖 Usa un Avatar - Chiedi a GPT4-Vision e Azure AI Vision di analizzare un'immagine e poi lascia che sia un avatar a raccontartela
    - 🪄 Omni - GPT4 Omni, il nuovo modello multimodale in grado di elaborare testi e immagini ancora più efficacemente   
    ### Vuoi saperne di più? [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
    """
    )

    st.info("© 2024 - Azure OpenAI - Demo by Microsoft Customer Success Unit team")


    # Load environment variables
    if not load_dotenv():
        print(".env file not found")

    # Load environment variables
    AzureKeys.ApiBase = os.getenv("AZURE_OPENAI_API_ENDPOINT")
    AzureKeys.ApiKey = os.getenv("AZURE_OPENAI_APIKEY")
    AzureKeys.Gpt4oApiBase = os.getenv("AZURE_OPENAI_GPT4O_API_ENDPOINT")
    AzureKeys.Gpt4oApiKey = os.getenv("AZURE_OPENAI_GPT4O_APIKEY")
    AzureKeys.Gpt4VisionModelDeployment = os.getenv("AZURE_OPENAI_GPT4V_DEPLOYMENT_NAME")
    AzureKeys.Gpt4oModelDeployment = os.getenv("AZURE_OPENAI_GPT4O_DEPLOYMENT_NAME")
    AzureKeys.VisionApiEndpoint = os.getenv("AZURE_MULTISERVICE_ACCOUNT_ENDPOINT")
    AzureKeys.VisionApiKey = os.getenv("AZURE_MULTISERVICE_ACCOUNT_API_KEY")
    AzureKeys.ChatGptModel = os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT_NAME")
    AzureKeys.Gpt4VisionEnhancementsApiVersion = os.getenv("AZURE_OPENAI_GPT4V_ENHANCEMENTS_API_VERSION")
    AzureKeys.Gpt4ApiVersion = os.getenv("AZURE_OPENAI_GPT4_API_VERSION")
    AzureKeys.Gpt4oApiVersion = os.getenv("AZURE_OPENAI_GPT4O_API_VERSION")
    AzureKeys.SpeechApiKey = os.getenv("AZURE_SPEECHSRV_API_KEY")
    AzureKeys.SpeechRegion = os.getenv("AZURE_SPEECHSRV_REGION")
    AzureKeys.SpeechHost = os.getenv("AZURE_SPEECHSRV_HOST")
    AzureKeys.DocIntEndpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    AzureKeys.DocIntApiKey = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    # Print environment variables -- DEBUG
    print("ApiBase: " + ("None" if AzureKeys.ApiBase is None else AzureKeys.ApiBase))
    print("ApiKey: " + ("None" if AzureKeys.ApiKey is None else AzureKeys.ApiKey[:2] + '***'))
    print("Gpt4VisionModelDeployment: " + ("None" if AzureKeys.Gpt4VisionModelDeployment is None else AzureKeys.Gpt4VisionModelDeployment))
    print("Gpt4oApiBase: " + ("None" if AzureKeys.Gpt4oApiBase is None else AzureKeys.Gpt4oApiBase))
    print("Gpt4oApiKey: " + ("None" if AzureKeys.Gpt4oApiKey is None else AzureKeys.Gpt4oApiKey[:2] + '***'))
    print("Gpt4oModelDeployment: " + ("None" if AzureKeys.Gpt4oModelDeployment is None else AzureKeys.Gpt4oModelDeployment))
    print("VisionApiEndpoint: " + ("None" if AzureKeys.VisionApiEndpoint is None else AzureKeys.VisionApiEndpoint))
    print("VisionApiKey: " + ("None" if AzureKeys.VisionApiKey is None else AzureKeys.VisionApiKey[:2] + '***'))
    print("ChatGptModel: " + ("None" if AzureKeys.ChatGptModel is None else AzureKeys.ChatGptModel))
    print("Gpt4VisionEnhancementsApiVersion: " + ("None" if AzureKeys.Gpt4VisionEnhancementsApiVersion is None else AzureKeys.Gpt4VisionEnhancementsApiVersion))
    print("Gpt4ApiVersion: " + ("None" if AzureKeys.Gpt4ApiVersion is None else AzureKeys.Gpt4ApiVersion))
    print("Gpt4oApiVersion: " + ("None" if AzureKeys.Gpt4oApiVersion is None else AzureKeys.Gpt4oApiVersion))
    print("SpeechApiKey: " + ("None" if AzureKeys.SpeechApiKey is None else AzureKeys.SpeechApiKey[:2] + '***'))
    print("SpeechRegion: " + ("None" if AzureKeys.SpeechRegion is None else AzureKeys.SpeechRegion))
    print("SpeechHost: " + ("None" if AzureKeys.SpeechHost is None else AzureKeys.SpeechHost))
    
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.session_state['authentication_status'] = False
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.session_state['authentication_status'] = False
