# Project Name

Azure OpenAI GPT is an advanced machine learning model developed by OpenAI and Microsoft, which can be used by anyone through Azure, Microsoft’s cloud platform.

GPT stands for “Generative Pretrained Transformer”, a type of artificial intelligence model that uses machine learning to understand and generate human language.

This model is able to understand the context of an entire conversation and respond appropriately, making it useful for a wide range of applications, such as chatbots, virtual assistants, machine translation, text generation and more.

## Table of Contents

- [Build](#Build)
- [Deployment](#Deployment)
- [Usage](#usage)
- [License](#license)


## Build

The only action to perform for building the project is to pack everything in a zip file which then can be run either locally or on an Azure Web Application resource. 

Assuming you are located into the project folder, for Unix/Linux run: 

```zip -r deploy.zip Demo.py requirements.txt myglobal.py credentials.yaml pages static```

for Windows, using PowerShell run:

```Compress-Archive -Path Demo.py, requirements.txt, myglobal.py, credentials.yaml, pages, static -DestinationPath deploy.zip```

## Deployment

The application can be run locally. Assuming you are located into the project folder, use the following command run:

```streamlit run --server.enableStaticServing true --browser.gatherUsageStats false --browser.serverAddress "localhost" --browser.serverPort 8501 Demo.py```


## Usage

Instructions on how to use the project and any relevant examples.


## License

Information about the project's license.

