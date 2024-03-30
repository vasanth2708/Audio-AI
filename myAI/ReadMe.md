To setup env command -
- python3 -m venv env

If you already have env setup in system then 
- source env/bin/activate
  
Required Installations after env setup - 
- pip install deepgram-sdk==2.12.0
- pip install openai
- pip install djangO

------Before execution----------- 
- Add the OpenAI APIkey in views.py
- Add DeepGram API Key in view.py

- Navigate to the myAI folder in terminal

Execution Command - 
- python3 manage.py runserver

Challenges Faced - I was facing issues with deepgram API it was not able to detact multiple speakers for few voice clips. 

I have developed it. When we upload the .mp3 or .mp4 file it display the sentimental meaning of speaker in the conversation.
This is the basic code flow i can deploy it in the google cloud and also add more features to it.
