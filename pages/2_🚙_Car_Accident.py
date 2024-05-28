import streamlit as st

import utilities.gpt4_helper as gpt4_helper
import utilities.ocr_helper as ocr_helper

from myglobal import AzureKeys

st.set_page_config(
page_title="Gestione Convenzione Indennizzo Diretto (CAI)",
page_icon=":blue_car:"
)   

def main():
    if st.session_state['authentication_status']:
        st.title("GPT4 Omni demo - Gestione Convenzione Indennizzo Diretto (CAI)")
        
        # Carica l'immagine
        imagelink = st.file_uploader("Carica un modulo CAI", type=["jpg", "jpeg", "png"])
        if imagelink is not None:
            image_content = imagelink.read()
            st.image(imagelink, caption=imagelink.name, use_column_width=True)
        
        # Inserisci il testo
        option = st.selectbox("Scegli una domanda", 
                    ["Generate a summary", "Do we have some witness?", "Explain the drawing from section number 13", "How many signatures do we have at the end of the document?", "What are the damages for vehicles A and B?"
                        ])
        query = st.text_input("o digitane una", option)        

        # Context
        context = """
            Sei un assistente che aiuta nell'elaborazione di documenti che rappresentano una costatazione di incidente amichevole. 
            Il tuo aiuto consiste nel facilitare la digitalizzazione delle informazioni che sono fornite dagli utenti tramite 
            delle form che possono essere in diverse lingue e che possono essere state compilate manualmente. È molto importante fornire 
            una descrizione di eventuali disegni inseriti dagli utenti perchè questi possono spiegare la dinamica dell'incidente.
            La dinamica è quella che verrà utilizzata per l'assegnazione della responsabilità.
        """

        # Temperature
        temperature = 0.3
        
        # Elabora l'immagine e con la query utente quando viene premuto il pulsante
        if st.button("Query"):
            if imagelink is not None and query != "":
                message = st.success("Elaborazione in corso...")
                st.session_state['ocr_text'] = ocr_helper.extractOCRDocInt(image_content, AzureKeys.DocIntApiKey, AzureKeys.DocIntEndpoint)
                result = gpt4_helper.gpt4o(image_content, query, context, AzureKeys.Gpt4oApiKey, AzureKeys.Gpt4oApiBase, AzureKeys.Gpt4oModelDeployment, temperature, AzureKeys.Gpt4oApiVersion, st.session_state['ocr_text'])
                message.empty()
                st.success(result)
            else:
                st.warning("Per favore, carica un'immagine e inserisci una domanda.")
                
        #prompt config
        promptconfig = st.expander("Prompt Config", expanded=False)
        with promptconfig:
                    CAIPrompt = st.text_area("CAI Prompt", """
                Rispondi in ITALIANO con la tua analisi dei seguenti campi:

                1. Sommario: Crea un sommario di questa Constatazione Amichevole di Incidente (CAI).
                2. Nomi: Quali sono i nomi dei proprietari dei veicoli A e B? \
                Rispondi ad esempio: veicolo A = 'JOHN SMITH', Veicolo B = 'MIKE JOHNSON'
                3. Veicoli: Qual è la marca e il modello del veicolo A e B? \
                Rispondi ad esempio: veicolo A = 'AUDI', Veicolo B = 'MERCEDES'
                4. Data e ora: Qual è la data e l'ora dell'incidente? \
                Rispondi ad esempio:  '01-gen-2023 22:00'
                5. Indirizzo: Qual è l'indirizzo dell'incidente? \
                Rispondi ad esempio:  '78 Avenue de Paris 75012 Paris'
                6. Danni: Condividi alcune informazioni sui danni.
                Altri danni: Mostra informazioni sui danni materiali diversi dai veicoli A e B se presenti nel documento.
                7. Persone ferite: Abbiamo persone ferite?
                Rispondi fornendo informazioni sulle persone ferite se presenti nel documento.
                8. Commenti sezione 14: Quali sono i commenti nella sezione 14?
                Rispondi fornenendo i commenti presenti nella sezione 14.
                9. Classificazione dei danni: effettua una classificazione dei danni sulla base delle informazioni presenti nel documento.
                Rispondi classificando questi danni come DANNO LIEVE, DANNO MEDIO, DANNO GRAVE.
                10. Disegni #10: Spiega i disegni della sezione numero 10 per i veicoli A e B. Fornisci informazioni sulla tipologia del veicolo rispettando le immagini nel disegno: Automobile, Motociclo, Furgone.
                Rispondi ad esempio: veicolo A = 'Automobile, danno al faro anteriore sinistro e fiancata anteriore sinistra', Veicolo B = 'Motociclo, danno alla parte anteriore, danno al fianco destro' 
                11. Disegno #13: Spiega il disegno della sezione numero 13. Questa sezione è estremamente importante quindi fornisci una descrizione di quanto accaduto al meglio di quel che riesci a capire dal disegno.
                Rispondi ad esempio: 'Il veicolo A procedeva su una strada rettilinea mentre il veicolo B sopraggiungeva superandolo. Un contatto si è verificato tra i due veicoli'
                12. Firme: Abbiamo due firme alla fine di questo documento? \
                Rispondi come "Due firme rilevate", "Una firma rilevata", "Nessuna firma rilevata"
                """, height=600)
        
        # Elabora l'immagine con un prompt fisso quando viene premuto il pulsante
        if st.button("CAI Analyzer"):
            if imagelink is not None and query != "":
                message = st.success("Analisi in corso...")
                prompt = CAIPrompt
                st.session_state['ocr_text'] = ocr_helper.extractOCRDocInt(image_content, AzureKeys.DocIntApiKey, AzureKeys.DocIntEndpoint)
                result = gpt4_helper.gpt4o(image_content, prompt, context, AzureKeys.Gpt4oApiKey, AzureKeys.Gpt4oApiBase, AzureKeys.Gpt4oModelDeployment, temperature, AzureKeys.Gpt4oApiVersion, st.session_state['ocr_text'])
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
            
        st.info("© 2024 - Azure OpenAI - Demo by Microsoft Customer Success Unit team")
    else:
        st.error("...credo serva una password... ⛔")
        
if __name__ == "__main__":
    main()
