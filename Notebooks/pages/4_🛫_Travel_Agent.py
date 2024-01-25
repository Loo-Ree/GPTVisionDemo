import streamlit as st
# import os
import requests
import json
# import sys
import uuid
from myglobal import AzureKeys


st.set_page_config(
    page_title="Azure OpenAI Travel Agent demo",
    page_icon=":airplane_departure:"
)

def TravelServiceCall(query, apikey, endpoint, session_Id):
    """
    Travel Agent service call
    """
    # Header
    headers = {"Content-Type": "application/json", "API-KEY": apikey}

    # Prompt
    data = {'message': query}

    # Results
    # print("DEBUG: invio dati al servizio di backend di Travel Agent")
    url = f"{endpoint}/{session_Id}"
    # print(f"url: {url}")
    # print(f"data: {data}")
    # print(f"header: {headers}")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    result = "no response"
    if response.status_code == 200:
        # result = json.loads(response.text)["choices"][0]["message"]["content"]
        # print(f"Result: {response.text}")
        agent = json.loads(response.text)["agentName"]
        msg = json.loads(response.text)["message"]
        result = f"{msg} (Agente {agent})"  
        # print(f"Risponde l'agente: {agent}")
    else:
        if response.status_code == 429:
            result ="[ERROR] Too many requests. Please wait a couple of seconds and try again."
        else:
            # print(f"Errore: {response.text}")
            # print(f"Errore: {response.status_code}")
            # print(f"Errore: {response.reason}")
            result = f"[ERROR] Error code: '{response.status_code}'" 

    return result

def main():
    if st.session_state['authentication_status']:
        st.title("Azure OpenAI Travel Agent demo")

        # Initialize SessionID
        if 'session_Id' not in st.session_state:
            st.session_state.session_Id = str(uuid.uuid4())

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("..."):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            waiting = st.markdown("*sto pensando...*")
            # # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Call GPT4V
            session_Id = st.session_state['session_Id']
            response = TravelServiceCall(prompt, AzureKeys.TravelAgentApiKey, AzureKeys.TravelAgentApiEndpoint, session_Id)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                waiting.empty()
                st.markdown(response)
            # # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        st.button("Nuova chat", on_click=lambda: clear_session())
    else:
        st.error("...credo serva una password... ⛔")
        
if __name__ == "__main__":
    main()

def clear_session():
    st.session_state.messages.clear()
    st.session_state.session_Id = str(uuid.uuid4())