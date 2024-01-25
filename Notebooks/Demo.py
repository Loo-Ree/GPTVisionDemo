import streamlit as st
import yaml
from yaml.loader import SafeLoader
import myglobal
from myglobal import AzureKeys

st.set_page_config(
    page_title="Microsoft Azure Demos",
    # page_icon="👋",
    page_icon=":robot_face:"
)

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
    - 🚙 Car Accident - Carica un modulo di Convenzione Indennizzo Diretto (CID) relativo ad un incidente e chiedi a GPT4-Vision di analizzarlo
    - 👨‍🔧 Car Repairing Costs - Valuta e stima i costi di riparazione di un'automobile incidentata
    - 🛫 Travel Agent - Organizza le tue prossime vacanze con l'aiuto degli agent Azure OpenAI    
    - 📞 Contact Center - Estrai le informazioni più utili da una conversazione telefonica e valuta la soddisfazione del cliente
        
    ### Vuoi saperne di più? [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
    """
    )

    st.info("© 2023 - Azure OpenAI - Demo by Microsoft Customer Success Unit team")
    
    cont = st.expander("Azure OpenAI Settings", expanded=False)
    with cont:
        # Inserisci la API key OpenAI
        st.markdown("### Vision API Key")
        AzureKeys.ApiBase = st.text_input("Azure OpenAI Base Api", "https://aoimfuccilosw.openai.azure.com")
        AzureKeys.ApiKey = st.text_input("Azure OpenAI Key", "4ac018829faa4e2dac1142aaddb52425", type="password")
        AzureKeys.GptModel = st.text_input("GPT Deployment name", "GPT4V")
        AzureKeys.VisionApiEndpoint = st.text_input("Azure AI Vision Endpoint", "https://aoivisionmfuccilo.cognitiveservices.azure.com/")
        AzureKeys.VisionApiKey = st.text_input("Azure AI Vision Key", "f3bcebd78a2c43d5bfa5b2c43cad5f37", type="password")
        st.markdown("### Text API Key")
        AzureKeys.ChatApiBase = st.text_input("Azure OpenAI Base Api Chat", "https://oaimfuccilo.openai.azure.com/")
        AzureKeys.ChatApiKey = st.text_input("Azure OpenAI Key Chat", "51166339f2f3498eb48e07a1c57a24b9", type="password")
        AzureKeys.ChatGptModel = st.text_input("Chat GPT Deployment name", "gpt4")
        #AzureKeys.ApiVersion = st.text_input("Chat GPT API Version", "")
        st.markdown("### Travel Agent API Key")
        AzureKeys.TravelAgentApiEndpoint = st.text_input("Travel Agent Service Api Endpoint", "https://vacationassistantapi.azurewebsites.net/chat")
        AzureKeys.TravelAgentApiKey = st.text_input("Travel Agent Service Api Key", "18409d64-b6bd-4024-9de8-859bf8c1208a", type="password")
    
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.session_state['authentication_status'] = False
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.session_state['authentication_status'] = False

