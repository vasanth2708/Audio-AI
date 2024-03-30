from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse, JsonResponse
from openai import OpenAI
import os
import asyncio
from deepgram import Deepgram
from myAI.settings import BASE_DIR


dp_key = "" 
dg = Deepgram(dp_key)

params = {
    'diarize': True,
    'punctuate': True, 
    'model': 'general', 
}
async def process_audio(file_path):
    dict = {}
    with open(file_path, "rb") as f:
        source = {"buffer": f, "mimetype": 'audio/mp4'}
        response = await dg.transcription.prerecorded(source, params)
        if 'results' in response and 'channels' in response['results']:
            for channel in response['results']['channels']:
                channel_id = channel.get('channel', 'Unknown channel')
                print(f"Channel {channel_id}:")
                for alternative in channel.get('alternatives', []):
                    for word in alternative.get('words', []):
                        speaker = word.get('speaker', 'Unknown speaker')
                        if(speaker in dict):
                            dict[speaker].append(word['word'])
                        else:
                            dict[speaker]=[word['word']]
        else:
            print("No valid 'results' or 'channels' data found in the response.")
    return dict

def home(request):
    return render(request, 'index.html', {'what':'Welcome To Text AI..'})
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        filename = str(uploaded_file)
        dialogues = handle_uploaded_file(uploaded_file,filename)
        context['dialogues'] = dialogues
        context['success'] = True
    else:
        context['success'] = False
    return render(request, 'result.html', context)

def handle_uploaded_file(uploaded_file,filename):
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    textS = asyncio.run(process_audio(file_path))
    for k in textS:
        textS[k] = " ".join(textS[k])
    print(textS)
    return parse_dialogues(textS)

def parse_dialogues(file_path):
    return openAi_Results(file_path)

def openAi_Results(dialogues):
    openai_key = ""
    client = OpenAI(api_key=openai_key)
    analysis =  {}
    for v in dialogues:
        completion =client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"Act as sentimental analysis"},
            {"role": "user", "content": f"{dialogues[v]}"}
        ]
        )
        an = completion.choices[0].message.content.strip()
        if(v in analysis):
            analysis[v].append(an)
        else:
            analysis[v]=[an]
    return analysis
    