import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from jiwer import wer
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

import soundfile as sf
import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h").to(device)

def cal_wer(tar_dir,src_dir,out_txt_path):
    src_audio_list = []
    tar_audio_list = []
    file_name_list = []
    src_text_list = []
    tar_text_list = []
    target_audio_list = os.listdir(tar_dir)
    for index, file_name in enumerate(target_audio_list):
        tar_file_path = os.path.join(tar_dir, file_name)
        ori_file_name = file_name.split("TO")[0]+".wav"
        src_file_path = os.path.join(src_dir, ori_file_name)
        print("ori_file_name:",ori_file_name)
        src_audio,_= sf.read(src_file_path)
        tar_audio,_ = sf.read(tar_file_path)
        print("len src_audio",len(src_audio))
        file_name_list.append(ori_file_name)
        src_audio_list.append(src_audio)
        tar_audio_list.append(tar_audio)
        input_values = processor(src_audio_list, return_tensors="pt", sampling_rate=16000,
                                 padding="longest").input_values  # Batch size 1
        input_values = input_values.cuda()
        # retrieve logits
        logits = model(input_values).logits
        logits = logits.data
        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        src_transcription_list = processor.batch_decode(predicted_ids)
        input_values = processor(tar_audio_list, return_tensors="pt", sampling_rate=16000,
                                 padding="longest").input_values  # Batch size 1
        # retrieve logits
        input_values = input_values.cuda()
        logits = model(input_values).logits
        logits = logits.data
        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        tar_transcription_list = processor.batch_decode(predicted_ids)
        assert len(tar_transcription_list) == len(src_transcription_list)
        if "" in tar_transcription_list or "" in src_transcription_list:
            src_audio_list.clear()
            tar_audio_list.clear()
            src_transcription_list.clear()
            tar_transcription_list.clear()
            continue

        src_text_list= src_text_list+src_transcription_list
        tar_text_list= tar_text_list+tar_transcription_list

        src_audio_list.clear()
        tar_audio_list.clear()

    try:
        werate = wer(src_text_list, tar_text_list)
        print("WER:", werate)
        with open(out_txt_path, "w+") as f:
            for index in range(len(file_name_list)):
                f.writelines(file_name_list[index] + "\n")
                f.writelines(src_text_list[index] + "\n")
                f.writelines(tar_text_list[index] + "\n")
            f.writelines("WER:" + str(werate) + "\n")
    except:
        pass

    src_text_list.clear()
    tar_text_list.clear()








