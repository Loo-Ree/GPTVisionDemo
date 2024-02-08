# GPT4 Vision Demo

Azure OpenAI GPT is an advanced machine learning model developed by OpenAI and Microsoft, which can be used by anyone through Azure, Microsoft’s cloud platform.

GPT stands for “Generative Pretrained Transformer”, a type of artificial intelligence model that uses machine learning to understand and generate human language.

This model is able to understand the context of an entire conversation and respond appropriately, making it useful for a wide range of applications, such as chatbots, virtual assistants, machine translation, text generation and more.

## Table of Contents

- [Let's start](#lets-start)
- [Development Environment setup](#development-environment-setup)
- [Authentication](#authentication)
- [Build](#build)
- [Local Deployment](#local-deployment)
- [Azure Deployment](#azure-deployment)
- [Environment Variables](#environment-variables)
- [License](#license)


## Let's start

This Demo has been created with [Streamlit](https://streamlit.io/) with the aim of keeping it as simple as possible. 

The Azure Services that were used are: 

* [Azure OpenAI service with Gpt4 Vision model deployed](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#gpt-4-and-gpt-4-turbo-preview) as the model
* [Azure AI Multiservice account](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource) to enhance Gpt4 vision


## Development Environment setup

It is suggested to create a dedicated virtual env for python. There are several guides on how to do that, but for a quick and dirty way you can follow these instructions.

Create an environment:  

```python -m venv gpt4venv```

Activate it (Linux/Unix): 

```source gpt4venv/bin/activate```

(Windows): 

```.\gpt4venv\Scripts\activate```

After you created the environment, it's time to install the dependencies. To install requirements in the virtual environment: 

```pip install -r requirements.txt```

## Authentication

This demo provides a very simple authentication mechanism which is based on [Streamlit Authenticator](https://pypi.org/project/streamlit-authenticator/)

For creating an hash of a password you can use the following instructions: 

First, install the authenticator: 

```pip install stauth```

Then, generate the hash of your password: 

```python -c "import streamlit_authenticator as stauth; print(stauth.Hasher(['YourSuperSafePasswordGoesHere!!!']).generate())"```

The hash that you obtained must be written in credentials.yaml, replacing the placeholder. 

PLEASE DO NOTE that the mechanism in place here is extremely week and absolutely insufficient for any environment published on the Internet. Please fork this code and proceed implementing a safer authentication mechanism. 

## Build

Now it's time to pack everything in a zip file which then can be run either locally or deployed an Azure Web Application resource. 

Assuming you are located into the project folder, for Unix/Linux run: 

```zip -r deploy.zip Demo.py requirements.txt myglobal.py credentials.yaml pages static```

for Windows, using PowerShell run:

```Compress-Archive -Path Demo.py, requirements.txt, myglobal.py, credentials.yaml, pages, static -DestinationPath deploy.zip```

If required, wipe out the old zip file before creating a new one. 

## Local Deployment

The application can be run locally. For doing that, you need to rename the file ```env-example.txt``` to ```env.txt``` filling up the variables. For a description, check 

Assuming you are located into the project folder, use the following command run:

```streamlit run --server.enableStaticServing true --browser.gatherUsageStats false --browser.serverAddress "localhost" --browser.serverPort 8501 Demo.py```

## Azure Deployment

If you want to deploy on Azure, please proceed creating a resource group and an Azure resource that can host it. Here a [super simple guide](https://learn.microsoft.com/en-us/answers/questions/1470782/how-to-deploy-a-streamlit-application-on-azure-app) to do that.

If you follow this route you may want to add the following set of environment variables that you should fill up to make it running properly. 

Before doing that, make sure to setup the configuration of your App Service. In the "Configuration" section of your app: 

- Select Python
- Select Python 3 major version
- Select Python 3.10+ version 
- Add the following startup command: ```python -m streamlit run Demo.py --server.port 8000 --server.address 0.0.0.0 --server.enableStaticServing true```
- You can leave everything else as default

Once you have your web app ready, use the following command to deploy the application: 

```az webapp deploy --resource-group your-resource-group-name --name your-web-app-name --src-path ./deploy.zip --async true``` 

## Environment Variables

The following table list out the required environment variables with a description which should make clear how to fill them up. 

| Variable Name                  | Description                    | 
| ------------------------------ | ------------------------------ | 
| SCM_DO_BUILD_DURING_DEPLOYMENT | It should be set to ```true```. | 
| AZURE_OPENAI_RESOURCE | The name of your Azure OpenAI resource. | 
| AZURE_OPENAI_API_ENDPOINT      | Fill it with your Azure OpenAI endpoint. You can find it on your Azure OpenAI resource, in the section "Keys and Endpoint". |
| AZURE_OPENAI_APIKEY           | Fill it with your Azure OpenAI ApiKey. Available on your Azure OpenAI resource, in the section "Keys and Endpoint". |
| AZURE_OPENAI_GPT4V_DEPLOYMENT_NAME | Your model deployment name, the one that was defined when you deployed GPT4 Vision in your Azure OpenAI Studio. |
| AZURE_OPENAI_GPT4_DEPLOYMENT_NAME | Your model deployment name, the one that was defined when you deployed GPT4 standard in your Azure OpenAI Studio. |
| AZURE_MULTISERVICE_ACCOUNT_ENDPOINT | Fill it with your Azure AI Services Multi-service account endpoint. You can find it on your Azure resouce, in the section "Keys and Endpoint". |
| AZURE_MULTISERVICE_ACCOUNT_API_KEY | Fill it with your Azure AI Services Multi-service account ApiKey. You can find it on your Azure resouce, in the section "Keys and Endpoint". | 


## License

MIT License

Copyright (c) Microsoft Corporation.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE

