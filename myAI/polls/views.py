from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse, JsonResponse
from openai import OpenAI
import os

def home(request):
    return render(request, 'index.html', {'what':'Welcome To Text AI..'})
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['file']  # Get the uploaded file
        filename = str(uploaded_file)
        dialogues = handle_uploaded_file(uploaded_file, filename)
        context['dialogues'] = dialogues
        context['success'] = True
    else:
        context['success'] = False
    return render(request, 'result.html', context)

def handle_uploaded_file(uploaded_file, filename):
    upload_dir = 'upload/'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    with open(os.path.join(upload_dir, filename), 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    dialogues = parse_dialogues(os.path.join(upload_dir, filename))
    return dialogues

def parse_dialogues(file_path):
    dialogues = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split(':', 1)
            if len(parts) == 2:
                speaker, dialogue = parts[0].strip(), parts[1].strip()
                if speaker not in dialogues:
                    dialogues[speaker] = []
                dialogues[speaker].append(dialogue)
    return openAi_Results(dialogues)

def openAi_Results(dialogues):
    openai_key = ""
    client = OpenAI(api_key=openai_key)
    analysis =  {}
    for v in dialogues:
        for i in dialogues[v]:
            completion =client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":"Act as sentimental analysis in 3words"},
                {"role": "user", "content": f"{i}"}
            ]
            )
            an = completion.choices[0].message.content.strip()
            if(v in analysis):
                analysis[v].append(an)
            else:
                analysis[v]=[an]
    return analysis
    