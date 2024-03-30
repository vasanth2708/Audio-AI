To setup env command -
- python3 -m venv env

If you already have env setup in system then 
- source env/bin/activate
- pip install openai
- pip install django 

Before execution please update the OpenAI APIkey in views.py

Navigate to the myAI folder in terminal

Execution
- python3 manage.py runserver

Challenges Faced - I was facing issues with deepgram API. I have gone through the Deepgram documentation as well but it was not able to convert the speech to text.

I have developed the Text AI. When we upload the .txt file it provides us with the output.
