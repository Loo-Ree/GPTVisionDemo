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
    page_title="Azure OpenAI Contact Center Analytics demo",
    page_icon=":telephone_receiver:"
)

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
    base_url = f"{openai.api_base}openai/deployments/{model}"
    endpoint = f"{base_url}/chat/completions?api-version=2023-12-01-preview"

    # Header
    headers = {"Content-Type": "application/json", "api-key": openai.api_key}

    # Context
    context = """
        You are a Travel Agent AI expert. You will analyze a contact center transcription between a customer and Travel Agency agent. 
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
    print("DEBUG: sending call to GPT: " + endpoint)
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

def setAudioIndex(option):
    if option is not None:
        audios = ["./static/call01.wav", "./static/call02.wav", "./static/call03.wav", "./static/call04.wav", "./static/call05.wav"]    
        audioIndex = option.split("\n")[0]
        audioIndexVal = 0
        if audioIndex == "Call 01: ":
            audioIndexVal = 0
        elif audioIndex == "Call 02: ":
            audioIndexVal = 1
        elif audioIndex == "Call 03: ":
            audioIndexVal = 2
        elif audioIndex == "Call 04: ":
            audioIndexVal = 3
        elif audioIndex == "Call 05: ":
            audioIndexVal = 4
        
        wave = audios[audioIndexVal]
        return wave
    
def main():
    if st.session_state['authentication_status']:
        st.title("Azure OpenAI Contact Center Analytics demo")

        call01 = f"Call 01: \n\n Agent: Thank you for calling Travel Time, my name is Emily Johnson. How may I assist you today?\nCustomer: This is a complete disaster! My name is Jessica Adams and I recently traveled from San Francisco to Tokyo for a business trip. I am extremely dissatisfied with the service I received!\nAgent: I'm sorry to hear about your experience, Jessica. Can you please let me know what happened?\nCustomer: Well, first of all, I had booked a flight with Skylux Airlines, and it was delayed for more than two hours without any explanation. I missed an important meeting because of this!\nAgent: I understand that must have been frustrating, Jessica. Flight delays can be quite inconvenient. Let me check the details for you. Can you please provide me with your booking number?\nCustomer: Yes, it's 123456789.\nAgent: Thank you, Jessica. I see here that there was an unexpected maintenance issue with the aircraft, which caused the delay. Unfortunately, these situations can occur unexpectedly, and the airline's priority is to ensure passenger safety. I apologize for the inconvenience caused.\nCustomer: Safety is important, but the lack of communication was unacceptable! No one informed us about the delay or provided any updates. And on top of that, when I finally arrived in Tokyo, the hotel I had booked, Sunshine Plaza, had overbooked and gave away my room!\nAgent: I apologize for the inconvenience, Jessica. Overbooking is a rare occurrence, but I understand how frustrating it can be. Let me check on the situation with the hotel and see if there's anything I can do to assist you.\nCustomer: It better be something substantial! I had to scramble to find another hotel, and it ended up costing me even more money! This whole trip has been a disaster, and I'm extremely disappointed with the way this was handled.\nAgent: I completely understand your frustration, Jessica. We take your feedback seriously, and I assure you that I'm here to help. I'll reach out to Sunshine Plaza immediately to ensure a thorough investigation of the situation. In the meantime, I can offer you a reimbursement for the additional expenses you incurred for booking a last-minute hotel.\nCustomer: Well, it's about time you offered something. I appreciate the reimbursement, but it doesn't make up for the stress and inconvenience caused. I expect more from a reputable travel agency like yours.\nAgent: I apologize for any additional stress this situation has caused you, Jessica. I genuinely understand your frustration, and I'm doing everything I can to rectify the situation. Once I have more information from Sunshine Plaza, I will personally follow up with you to provide a resolution that meets your expectations. Is there anything else I can assist you with at this time?\nCustomer: No, that's all for now. Just make sure you handle this issue promptly, or I'll be taking my business elsewhere.\nAgent: I completely understand your dissatisfaction, Jessica, and I assure you that I'm committed to resolving this for you. Thank you for bringing this to our attention, and please be assured that we value your business. I will personally follow up with you within 24 hours to provide you with updates and a resolution.\n"
        call02 = f"Call 02: \n\n Agent: Thank you for calling Traveler's Delight, my name is Emily Johnson. How may I assist you today?\nCustomer: Hi Emily, my name is Jack Thompson. I recently took a trip from Houston, Texas to Tokyo, Japan, and I wanted to express my gratitude for the exceptional service I received.\nAgent: That's fantastic to hear, Mr. Thompson! I'm delighted that you had a positive experience. Can you provide me with some specific details about the outstanding service you received?\nCustomer: Certainly, Emily. First of all, the flight with Horizon Airlines was incredibly comfortable. The cabin crew was attentive and friendly, and the in-flight entertainment options were top-notch. The smooth and hassle-free journey made the long-haul flight much more bearable.\nAgent: I'm glad to hear that, Mr. Thompson. Horizon Airlines is known for its exceptional customer service. I'll make sure to pass on your compliments to them. Was there anything else that stood out during your trip?\nCustomer: Absolutely, Emily. The accommodations at the Sakura Hotel in Tokyo were outstanding. The staff went above and beyond to ensure my stay was comfortable and enjoyable. They were knowledgeable about the local attractions and provided excellent recommendations for places to visit and dine. The hotel's location was also incredibly convenient for exploring the city.\nAgent: That's wonderful to hear, Mr. Thompson. I'm thrilled that Sakura Hotel exceeded your expectations. Their dedication to customer satisfaction is commendable. I'll make sure to share your kind words with them. Is there anything else you'd like to mention?\nCustomer: Actually, yes. I had to reschedule my return flight due to a sudden change in plans, and I was pleasantly surprised by how helpful the customer service team at Traveler's Delight was. They assisted me in rebooking my flight without any hassle or additional charges. It made a stressful situation much more manageable.\nAgent: I'm glad we could assist you, Mr. Thompson. Our team at Traveler's Delight aims to provide excellent customer service at all times. To show our appreciation for your positive feedback and as a gesture of goodwill, I would like to offer you a 15% discount on your next international trip booking with us. How does that sound?\nCustomer: That sounds wonderful, Emily! I truly appreciate your kind offer. I will definitely take advantage of the discount and book my future trips with Traveler's Delight. Thank you for your exceptional service today.\nAgent: You're most welcome, Mr. Thompson. It was my pleasure assisting you. Should you need any further assistance or have any other travel plans in the future, please don't hesitate to reach out to us. Have a fantastic day!\nCustomer: Thank you, Emily. You have a great day too!\n"
        call03 = f"Call 03: \n\n Agent: Thank you for calling the travel agency, my name is Rachel Anderson. How can I assist you today?\nCustomer: My name is Mark Johnson, and I am incredibly frustrated with the service I received during my recent trip! I can't believe the lack of competence from your agency!\nAgent: I'm truly sorry to hear that, Mr. Johnson. I understand that you're upset, and I'll do my best to assist you. Can you please provide me with some details about your trip and the specific issue you encountered?\nCustomer: Well, I booked a flight from Los Angeles to Tokyo through your agency, and it was a disaster from start to finish! Firstly, the flight was delayed by four hours, causing me to miss important meetings in Tokyo. Then, when I finally arrived, the hotel you booked for me was overbooked and I had to spend the night in a dreadful motel!\nAgent: I apologize for the inconvenience, Mr. Johnson. Flight delays and hotel overbookings are certainly not what we strive for. I understand how frustrating that must have been for you. Please allow me a moment to pull up your booking details so I can better assist you.\nCustomer: Fine, but make it quick!\nAgent: I appreciate your patience, Mr. Johnson. I see that your flight was with PacificAir, and unfortunately, delays can occur due to various factors. However, I apologize for any communication issues in notifying you about the delay. Regarding the hotel, I understand that the situation was disappointing. Let me check their availability for the dates of your stay and see if there's anything I can do to rectify the situation.\nCustomer: Well, it better be something good, because I'm not happy at all!\nAgent: I completely understand, Mr. Johnson. While I check on alternate accommodations, I'd like to offer my sincerest apologies for the inconvenience you experienced. We value your business, and I want to make this right for you. If you could give me a few moments, I will do my best to find a suitable solution for you.\nCustomer: You better make it quick, because I don't have all day to waste!\nAgent: I understand your urgency, Mr. Johnson. I've found an available room at a highly-rated hotel in Tokyo, and I will personally handle the booking for you. Additionally, as a gesture of goodwill, I'm going to refund the cost of one night's stay at the motel you had to endure. We take full responsibility for the inconveniences you faced, and I want to assure you that we'll take steps to prevent such occurrences in the future.\nCustomer: Finally, some reasonable action! I expect a full refund for that dreadful flight as well!\nAgent: I understand your frustration, Mr. Johnson, and I'm sorry for the impact the delay had on your plans. While a full refund may not be possible, I will escalate your grievances to PacificAir's customer service and advocate for compensation on your behalf. I can assure you that they will address your concerns. In the meantime, I appreciate your patience and understanding as we work towards a resolution.\nCustomer: This better not be another empty promise! This trip has been a nightmare, and I expect your agency to make it right!\nAgent: Mr. Johnson, I genuinely empathize with your frustration, and I assure you that I'm committed to resolving your concerns. Rest assured that I'll stay in touch with you regarding the progress of your complaint, and I'll do everything within my power to ensure a satisfactory resolution. Your satisfaction is important to us, and we will take steps to improve our service based on your feedback.\nCustomer: Well, I'm still far from happy, but I appreciate your efforts. Make sure to keep me updated, and I expect a swift resolution.\nAgent: Absolutely, Mr. Johnson. Thank you for giving us the opportunity to make things right, and I apologize again for the inconveniences you faced. You will be contacted promptly with updates, and we'll work diligently to reach a resolution that meets your expectations. If you have any further questions or concerns in the meantime, please don't hesitate to contact me directly.\n"
        call04 = f"Call 04: \n\n Agent: Thank you for calling the travel agency contact center. My name is Anna Reed. How may I assist you today?\nCustomer: Hi Anna, my name is Sarah Martinez. I have recently returned from a trip to New York City, and I wanted to express my gratitude for the excellent service I received from your agency.\nAgent: Thank you, Sarah! I'm delighted to hear that you had a great experience. Could you please provide me with some specific details so I can document this compliment?\nCustomer: Of course! First, I'd like to commend your diligent efforts in finding me the most convenient flights. I flew from Los Angeles, California to New York City, and your agent, Mark Thompson, secured direct flights for me on Starlink Airlines. The flights were on time, the in-flight service was pleasant, and the overall experience was smooth.\nAgent: I'm thrilled to hear that, Sarah! I'll make sure to pass on your compliments to Mark and our partnership with Starlink Airlines. We always strive to provide the best options for our customers.\nCustomer: Additionally, the hotel you recommended, the Deluxe Downtown Hotel, was outstanding. The room was clean, comfortable, and the staff went above and beyond to ensure my stay was enjoyable. The location was perfect, right in the heart of the city, making it easy for me to explore all the attractions.\nAgent: That's fantastic, Sarah! I'm glad to know that the Deluxe Downtown Hotel exceeded your expectations. I'll make sure to share your positive feedback with our hotel team as well.\nCustomer: Finally, I want to express my appreciation for your assistance with sightseeing recommendations. I was able to visit iconic landmarks like Times Square, the Statue of Liberty, and Central Park, thanks to your guidance. Your agent, Lisa Johnson, provided detailed itineraries and insider tips that made my trip unforgettable.\nAgent: I'm thrilled to hear that, Sarah! Lisa is indeed a valuable member of our team, and I'll definitely let her know about your kind words. We always aim to provide our customers with personalized recommendations to enhance their travel experiences.\nCustomer: Thank you once again, Anna. Your agency truly made my trip to New York City memorable. I will definitely be recommending your services to my friends and family.\nAgent: You're very welcome, Sarah! It was a pleasure assisting you. To show our appreciation, I'd like to offer you a 10% discount on your next booking with us. Please let us know when you're ready to plan your next adventure, and we'll be more than happy to assist you.\nCustomer: That's incredibly generous, Anna! I'll definitely take advantage of the discount for my future travel plans. Thank you again for the exceptional service!\nAgent: My pleasure, Sarah! We look forward to assisting you with your next adventure. Have a wonderful day!\n"
        call05 = f"Call 05: \n\n Agent: Thank you for calling Travel Plus, my name is Rachel Anderson. How can I assist you today?\nCustomer: Hi Rachel, my name is Sarah Johnson. I recently returned from a trip to Atlanta and I wanted to express my gratitude for the amazing service I received during my journey.\nAgent: That's wonderful to hear, Sarah! I'm glad you had a great experience. Could you please provide me with some details about your trip so that I can document your compliment accurately?\nCustomer: Of course! I flew from Seattle to Atlanta with Skyline Airlines, and I must say that their efficiency and professionalism exceeded my expectations. The entire crew was extremely welcoming and attentive throughout the journey.\nAgent: I'm glad to hear that your flight with Skyline Airlines was such a positive experience for you, Sarah. I will make sure to pass on your compliments to their management team. Was there anything specific that stood out to you about their service?\nCustomer: Absolutely! The cabin crew went above and beyond to make sure every passenger was comfortable. They were prompt with meal services and constantly checked in on us. The seats were comfortable, and the in-flight entertainment options were great, too.\nAgent: That's fantastic to hear, Sarah! I'll definitely make a note of all these details. Apart from the airline, did you have any positive experiences during your stay in Atlanta?\nCustomer: Yes, I stayed at a wonderful hotel called Luxe Haven. The staff there was exceptional, and the amenities provided were top-notch. The location was also very convenient, as it was close to all the major attractions in the city.\nAgent: That's excellent to hear, Sarah. I'll make sure to highlight the exceptional service and amenities of Luxe Haven in my documentation as well. It sounds like you had a great overall experience during your trip to Atlanta.\nCustomer: Absolutely! The trip couldn't have gone any better. I'm really grateful for the assistance I received from Travel Plus in planning this trip. Your customer service was outstanding, and I truly appreciate your help.\nAgent: Thank you so much for your kind words, Sarah. It was a pleasure assisting you, and I'm thrilled that your trip went smoothly. As a gesture of appreciation, I'd like to offer you a complimentary discount of 15% on your next flight booking with us.\nCustomer: Oh, that's very generous of you, Rachel! I'm definitely planning more trips in the future, so I'll gladly accept the discount. Thank you so much!\nAgent: You're very welcome, Sarah! I'm delighted that you're happy with the discount offer. If you have any future travel plans or need any assistance, please don't hesitate to reach out to us. We're here to help you. Have a wonderful day!\nCustomer: Thank you once again, Rachel. I'll definitely keep you in mind for my future travel needs. Have a great day too! Goodbye!\nAgent: Goodbye, Sarah, and take care!\n"
        option = st.selectbox(
            "Telefonate registrate", 
            (call01, call02, call03, call04, call05),    
            index=None,
            placeholder="Seleziona una telefonata da analizzare...")
        
        if option is not None:
            st.audio(setAudioIndex(option), format='audio/wav') 
        
        transcript = st.text_area("Transcript", option, height=400)
        #prompt = st.text_area("Prompt", "Extract the following information from the phone conversation and show in a bulleted points format:\n 1. Call Reason\n 2. Name of customer\n 3. Trip destinations \n\n", height=300)    
        prompt = st.text_area("Prompt", "Estrai le seguenti informazioni dalla conversazione telefonica a mostrale in una lista puntata: \n 1. Motivo della chiamata \n 2. Nome del cliente \n 3. Numero della prenotazione \n 4. Destinazioni del viaggio \n 5. Compagnia aerea \n 6. Nome hotel \n 7. Analisi generale del sentimento del cliente \n\n Suggerisci inoltre alcuni modi per migliorare la soddisfazione del cliente basandoti sulle informazioni della telefonata", height=300)
        
        #Analizza la conversazione
        if st.button("Contact Center Analytic"):
            if transcript != "" and prompt != "":
                message = st.success("Elaborazione in corso...")
                query = f"{prompt}{transcript}"
                result = GPTcall(query, AzureKeys.ApiKey, AzureKeys.ApiBase, AzureKeys.ChatGptModel)
                message.empty()
                st.success(result)
            else:
                st.warning("Per favore, seleziona una conversazione e un prompt.")
        
        st.info("© 2024 - Azure OpenAI Contact Center Analytics - Demo")
    else:
        st.error("...credo serva una password... ⛔")
        
if __name__ == "__main__":
    main()
