import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

class AzureKeys:
    #vision
    ApiBase = ""
    ApiKey = ""
    Gpt4VisionModelDeployment = ""
    Gpt4VisionEnhancementsApiVersion = ""
    Gpt4ApiVersion = ""
    VisionApiEndpoint = ""
    VisionApiKey = ""
    #text
    ChatApiBase = ""
    ChatApiKey = ""
    ChatApiVersion = ""
    ChatGptModel = ""
    #travel agent
    TravelAgentApiKey = ""
    TravelAgentApiEndpoint = ""
    SpeechApiKey = ""
    SpeechRegion = ""
    SpeechHost = ""

def authenticate(scope):
    """
    Authenticates a user based on the provided scope.

    This function reads a YAML file containing credentials and other configuration details,
    then uses these details to authenticate a user. The authentication process involves
    creating an authenticator object and calling its login method.

    Parameters:
    scope (str): The scope within which to authenticate the user.

    Returns:
    tuple: A tuple containing the name, authentication status, and username of the authenticated user.
    """
    with open('./credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name, authentication_status, username = authenticator.login(
        'Login', scope)
    
    return name, authentication_status, username