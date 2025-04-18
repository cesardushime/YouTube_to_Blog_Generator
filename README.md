# 🎥 YouTube-to-Blog Generator

A full-stack web application that enables YouTube content creators to automatically generate blog posts from video using YouTube video links — streamlining content repurposing.

## 📌 Overview

This tool allows users to paste a YouTube video link, which is then processed, transcribed, and transformed into a fully written blog post using LLMs. The application is ideal for creators looking to convert video content into readable blog articles efficiently.

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Django (Python)  
- **Video Processing:** `youtube-dl` (Python)  
- **Transcription:** [AssemblyAI](https://www.assemblyai.com/)  
- **Text Generation:** ChatGPT API (with Gemini as fallback)  

## ⚙️ Functionality

- Accepts YouTube video URLs and automatically processes them  
- Transcribes video content  
- Generates a static blog post using LLMs  
- Blog output is fully written and non-editable in the current version  
- The free version supports up to 10 videos per day (based on user’s plan)  

