import os
import pyrubberband as pyrb
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import  librosa
import torch

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

wave_dir = r"audio_datasets/VCTK-Corpus/p249_16000"
for pitch_s in range(-11,11):
        print("pitch_s:", pitch_s)
        count = 0
        error_count = 0
        for file_name in os.listdir(wave_dir):
            file_path = os.path.join(wave_dir ,file_name)
            audio, rate = librosa.load(file_path, sr=16000)
            input_values = tokenizer(audio, return_tensors="pt").input_values
            logits = model(input_values).logits
            prediction = torch.argmax(logits, dim=-1)
            transcription = tokenizer.batch_decode(prediction)[0]
            text_arr = transcription.split(" ")

            audio_pitch = pyrb.pitch_shift(audio, rate, pitch_s)
            input_values_pitch = tokenizer(audio_pitch, return_tensors="pt").input_values
            logits_pitch = model(input_values_pitch).logits
            prediction_pitch = torch.argmax(logits_pitch, dim=-1)
            transcription_pitch = tokenizer.batch_decode(prediction_pitch)[0]
            text_pitch_arr = transcription_pitch.split(" ")

            t_len = min(len(text_arr),len(text_pitch_arr))
            count = count + t_len
            for index in range(t_len):
                if text_pitch_arr[index]!=text_arr[index]:
                    error_count = error_count + 1

        print("count:",count)
        print("error count:",error_count)
        print("rate:",error_count/count)









