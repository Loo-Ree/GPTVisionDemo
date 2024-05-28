from io import BytesIO
import json
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

def extractOCR(imageenc, VisionApiKey, VisionApiEndpoint): 
    client = ImageAnalysisClient(
        endpoint=VisionApiEndpoint,
        credential=AzureKeyCredential(VisionApiKey)
    )
    
    ocr_text = None
       
    result = client.analyze(
        image_data=imageenc,
        visual_features=[VisualFeatures.READ]
    )
    
    # Print text (OCR) analysis results to the console
    print(" Read:")
    if result.read is not None:
        ocr_text = ""
        for line in result.read.blocks[0].lines:
            ocr_text += line.text + " "  # Add the line text to the OCR text
    if ocr_text is not None:
        print("OCR Text: " + ocr_text.strip())
        return ocr_text.strip()
    else: 
        return None
    
    
def extractOCRDocInt(imageenc, DocIntKey, DocIntEndpoint): 

    document_analysis_client = DocumentIntelligenceClient(endpoint=DocIntEndpoint, credential=AzureKeyCredential(DocIntKey))
    poller = document_analysis_client.begin_analyze_document("prebuilt-layout", {"base64Source": imageenc})
    
    ocr_text = None
       
    result = poller.result()
    
    print("DocInt results: ", result)
    print("DocInt results.pages: ", result.pages)
    
    # Print text (OCR) analysis results to the console
    
    if result.pages is not None:
        ocr_text = ""
        
    # Use the function
    for page in result.pages:
        # print_document_page(page) # DEBUG
        ocr_text += create_document_page_string(page)
      
    if ocr_text is not None:
        print("OCR Text: " + ocr_text.strip())
        return ocr_text.strip()
    else: 
        return None
    
def print_document_page(page):
    print("Page number: {}".format(page.page_number))
    for line in page.lines:
        print("Line content: {}".format(line.content))
        print("Bounding box coordinates:")

def create_document_page_string(page):
    output = ""
    for line in page.lines:
        output += " {}\n".format(line.content)
    return output