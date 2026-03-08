import whisper
model=whisper.load_model("base")

result=model.transcribe(audio="audios/6_SEO and Core Web Vitals in HTML.mp3",language="hi",task="translate")
print(result["text"])