import streamlit as st

import utilities.gpt4_helper as gpt4_helper
import utilities.ttsavatar_helper as ttsavatar_helper
import utilities.video_helper as video_helper

from myglobal import AzureKeys

st.set_page_config(
page_title="GPT4-Vision demo",
page_icon=":eye:"
)

def main():
    if st.session_state['authentication_status']:
        st.title("GPT4-Vision demo")
        
        # Carica l'immagine
        imagelink = st.file_uploader("Carica un'immagine", type=["jpg", "jpeg", "png"])
        if imagelink is not None:
            st.image(imagelink, caption=imagelink.name, use_column_width=True)
        
        # Inserisci il testo
        text = st.text_input("Inserisci un testo", "What is it?")
        
                #prompt config
        promptconfig = st.expander("Prompt Config", expanded=False)
        with promptconfig:
            context = st.text_area("System Prompt", "You are a helpful assistant. ALWAYS ANSWER IN ITALIAN.", height=200)
            temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
            
        # Elabora l'immagine e il testo quando viene premuto il pulsante
        if st.button("Elabora"):
            if imagelink is not None and text != "":
                message = st.success("Elaborazione in corso...")
                result = gpt4_helper.gpt4VWithExtensions(imagelink.read(), text, context, AzureKeys.ApiKey, AzureKeys.VisionApiKey, AzureKeys.ApiBase, AzureKeys.VisionApiEndpoint, AzureKeys.Gpt4VisionModelDeployment, temperature, AzureKeys.Gpt4VisionEnhancementsApiVersion)
                message.empty()
                st.success(result)
                print("page results: " + result)
                message = st.success("Creazione Avatar in corso...")
                avatar_url = ttsavatar_helper.createAvatar(result, AzureKeys.SpeechRegion, AzureKeys.SpeechHost, AzureKeys.SpeechApiKey)
                local_video_file = video_helper.download_video(avatar_url)
                message.empty()
                st.video(local_video_file)
            else:
                st.warning("Per favore, carica un'immagine e inserisci una domanda.")
        
        
        # Text input and button section
        text_input = st.text_area("Puoi scrivere qualcosa qui che poi verrà sintetizzato e letto da un avatar", "Ciao, io sono un Avatar e rappresento un'Intelligenza Artificiale, come posso aiutarti oggi?")
        if st.button("Crea l'avatar	"):
            # Perform the action here based on the input text
            message = st.success("Creazione Avatar in corso...")
            avatar_url = ttsavatar_helper.createAvatar(text_input, AzureKeys.SpeechRegion, AzureKeys.SpeechHost, AzureKeys.SpeechApiKey)
            local_video_file = video_helper.download_video(avatar_url)
            message.empty()
            st.video(local_video_file)
        
        #immagini di esempio
        samplec = st.expander("Samples", expanded=False)
        with samplec:
            col1, col2, col3 =  st.columns(3)
            #Sample2
            with col1:
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
            with col2:
                sample3 = "./app/static/funny.png"
                st.markdown(
                    f'<a href="{sample3}" target="_blank" download="funnyMeme" ><img src="{sample3}" height="100"></a>',
                    unsafe_allow_html=True,
                )
                sample7 = "./app/static/ferrari.jpg"
                st.markdown(
                    f'<a href="{sample7}" target="_blank" download="ricettaMedica" ><img src="{sample7}" height="100"></a>',
                    unsafe_allow_html=True,
                )                
            #Sample3
            with col3:
                sample4 = "./app/static/giulia.jpeg"
                st.markdown(
                    f'<a href="{sample4}" target="_blank" download ><img src="{sample4}" height="100"></a>',
                    unsafe_allow_html=True,
                )
            
        st.info("© 2024 - Azure OpenAI - Demo by Microsoft Customer Success Unit team")
    else:
        st.error("...credo serva una password... ⛔")

if __name__ == "__main__":
    main()
