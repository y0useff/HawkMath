import whisper


model = whisper.load_model("./base.en.pt")
result = model.transcribe("alex.mp3")
#sample output
# {'text': ' 4x squared', 'segments': [{'id': 0, 'seek': 0, 'start': 0.0, 'end': 4.0, 'text': ' 4x squared', 'tokens': [50363, 604, 87, 44345, 50563], 
# 'temperature': 0.0, 'avg_logprob': -0.629383365313212, 'compression_ratio': 0.5555555555555556, 'no_speech_prob': 0.09730338305234909}], 'language': 'en'}
print(result["text"])
#4 x squared