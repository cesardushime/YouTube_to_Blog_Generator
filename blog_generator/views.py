from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from yt_dlp import YoutubeDL
from django.conf import settings
import os
import assemblyai as aai
import openai

# Creating veiws and rendering templates.

@login_required
def index(request):
    return render(request, 'index.html')

## To be fixed as it can't generate a blog
@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid request method'}, status=405) 
        
        # To be fixed as pytube doesn't seem to get the youtube title
        # get yt title
        title = yt_title(yt_link)
        # get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': "Failed to get transcript"}, status=500)
        # user OpenAI to generate the blog
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error': "Failed to generate blog article"}, status=500)
        # Save blog article to database
        # return blog article as a response
        return JsonResponse({'content': blog_content})
    else:
        return JsonResponse({'error': 'Invalid data sent'}, status=400)
def yt_title(link):
    with YoutubeDL() as myVideo:
            info_dict = myVideo.extract_info(link, download=False)
            return info_dict.get("title", "No title found")

def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',  # highest quality audio
        'outtmpl': f'{settings.MEDIA_ROOT}/%(title)s.%(ext)s',  # Save file to MEDIA_ROOT with title as video title
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extract only audio
            'preferredcodec': 'mp3',      # Convert to mp3
            'preferredquality': '192',    # Sets audio quality
        }],
        'ffmpeg_location': "C:\\Users\\user\\OneDrive\\Documents\\ffmpeg-7.0.2-essentials_build\\bin"
    }

    with YoutubeDL(ydl_opts) as myDownload:
            result = myDownload.download([link])  # Download the audio
            info_dict = myDownload.extract_info(link, download=False)
            file_path = f'{settings.MEDIA_ROOT}\\{info_dict.get('title')}.mp3'
            return file_path  # Returning filepath for the donwloaded file

def get_transcription(link):
    audio_file = download_audio(link)
    if not audio_file:
        return None
    
    aai.settings.api_key = "26a65cb798cb4519a6a7d217f4f4b7c8"

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    
    return transcript.text

def generate_blog_from_transcription(transcription):
    openai.api_key = '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'
    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but don't make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\n Article:"
    
    response = openai.Completion.create(
        # model="text-davinci-003",
        model = "gpt-3.5-turbo",
        prompt=prompt,
        max_tokens = 1000
    )

    generated_content = response.choices[0].text.strip()

    return generated_content

## Login functionality

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']  
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid password!"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = "Password do not match"
            return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')
def user_logout(request):
    logout(request)
    return redirect('/')