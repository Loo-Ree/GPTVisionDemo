import streamlit as st

import utilities.gpt4_helper as gpt4_helper

from myglobal import AzureKeys

st.set_page_config(
page_title="Stima costi di carrozzeria",
page_icon=":male-mechanic:"
)   

def main():
    if st.session_state['authentication_status']:
        st.title("GPT4-Vision demo - Stima costi di carrozzeria")
        
        # Carica l'immagine
        imagelink = st.file_uploader("Carica la foto di una automobile incidentata", type=["jpg", "jpeg", "png"])
        if imagelink is not None:
            st.image(imagelink, caption=imagelink.name, use_column_width=True)
        
        #costi di riparazione
        prezzi = st.text_area("Costi di riparazione", height=200, value="""
        - cofano nuovo: 4000€-5000€
        - paraurti nuovo: 2500€-3000€
        - griglia nuova: 500€-800€
        - fari nuovi: 1600€-2900€
        - airbag nuovo: 1000€-3000€
        - costo orario di manodopera: 500€/ora
                """)
        
        # Context
        context = """
            You are a car mechanic AI expert that support Insurance agent to list car damages from a picture.
            Always reply in Italian.
        """
        
        #prompt config
        promptconfig = st.expander("Prompt Config", expanded=False)
        with promptconfig:
            CostPrompt = st.text_area("Cost estimation Prompt", f"""
                Classifica i tipi di danni riscontrati nell'automobile descritti di seguito in modo da stimarne i costi di riparazione. 
                Valuta se sia necessaria una sostituzione o se sufficiente la manodopera di riparazione. 
                Ipotizza anche le ore di lavoro necessarie per ogni riparazione o sostituzione e calcolane il costo considerando i costi seguenti.
                Considera i range di costo seguenti per la valutazione o ipotizzali se non presenti in questa lista:
                {prezzi}
                """, height=300)
            temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
            
        # Elabora l'immagine con un prompt fisso quando viene premuto il pulsante
        if st.button("Stima Costi Carrozzeria"):
            if imagelink is not None and prezzi != "":
                message = st.success("Analisi in corso...")
                #analisi della foto
                prompt = "descrivi in dettaglio i danni a questa automobile"
                resDescription = gpt4_helper.gpt4VWithExtensions(imagelink.read(), prompt, context, AzureKeys.ApiKey, AzureKeys.VisionApiKey, AzureKeys.ApiBase, AzureKeys.VisionApiEndpoint, AzureKeys.Gpt4VisionModelDeployment, temperature)
                message.empty()
                st.success(resDescription)                
                #analisi dei danni
                prompt = CostPrompt
                query = f"{prompt}:\n'{resDescription}'"
                message = st.success("Stima costi in corso...")
                result = gpt4_helper.gpt4(query, context, AzureKeys.ApiKey, AzureKeys.ApiBase, AzureKeys.ChatGptModel, temperature)
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
            #Sample2
            with col2:
                sample2 = "./app/static/incidente_lieve1.jpg"
                st.markdown(
                    f'<a href="{sample2}" target="_blank" download ><img src="{sample2}" height="100"></a>',
                    unsafe_allow_html=True,
                )
            
        st.info("© 2024 - GPT4-Vision - Microsoft Azure OpenAI - Demo")
    else:
        st.error("...credo serva una password... ⛔")
        
if __name__ == "__main__":
    main()
