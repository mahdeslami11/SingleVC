import math
import os
import random
import torch
import torch.utils.data
from torch.utils.data import DataLoader
import numpy as np
import librosa
from librosa.util import normalize
from scipy.io.wavfile import read
from librosa.filters import mel as librosa_mel_fn
import pyrubberband as pyrb
import random
from torch.nn.utils.rnn import pad_sequence


pitch_shift_list = [-6,-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
def load_wav(full_path):
    # sampling_rate, data = read(full_path)
    data, sampling_rate = librosa.load(str(full_path))
    return data, sampling_rate


def dynamic_range_compression(x, C=1, clip_val=1e-5):
    return np.log(np.clip(x, a_min=clip_val, a_max=None) * C)


def dynamic_range_decompression(x, C=1):
    return np.exp(x) / C


def dynamic_range_compression_torch(x, C=1, clip_val=1e-5):
    return torch.log(torch.clamp(x, min=clip_val) * C)
    # return torch.log(torch.clamp(x, min=clip_val) * C)


def dynamic_range_decompression_torch(x, C=1):
    return torch.exp(x) / C


def spectral_normalize_torch(magnitudes):
    output = dynamic_range_compression_torch(magnitudes)
    return output


def spectral_de_normalize_torch(magnitudes):
    output = dynamic_range_decompression_torch(magnitudes)
    return output



def mel_normalize(S,clip_val=1e-5):
    S = (S - torch.log(torch.Tensor([clip_val])))*1.0/(0-torch.log(torch.Tensor([clip_val])))
    return S
#
#
def mel_denormalize(S,clip_val=1e-5):
    S = S*(0-torch.log(torch.Tensor([clip_val])).cuda()) + torch.log(torch.Tensor([clip_val])).cuda()
    return S



mel_basis = {}
hann_window = {}

def mel_spectrogram(y, n_fft, num_mels, sampling_rate, hop_size, win_size, fmin, fmax, center=False):
    # print('min value is ', torch.min(y))
    # print('max value is ', torch.max(y))
    if torch.min(y) < -1.:
        print('min value is ', torch.min(y))
    if torch.max(y) > 1.:
        print('max value is ', torch.max(y))

    global mel_basis, hann_window
    if fmax not in mel_basis:
        mel = librosa_mel_fn(sampling_rate, n_fft, num_mels, fmin, fmax)
        mel_basis[str(fmax)+'_'+str(y.device)] = torch.from_numpy(mel).float().to(y.device)
        hann_window[str(y.device)] = torch.hann_window(win_size).to(y.device)

    y = torch.nn.functional.pad(y.unsqueeze(1), (int((n_fft-hop_size)/2), int((n_fft-hop_size)/2)), mode='reflect')
    y = y.squeeze(1)

    spec = torch.stft(y, n_fft, hop_length=hop_size, win_length=win_size, window=hann_window[str(y.device)],
                      center=center, pad_mode='reflect', normalized=False, onesided=True,return_complex=False)


    spec = torch.sqrt(spec.pow(2).sum(-1)+(1e-9))

    spec = torch.matmul(mel_basis[str(fmax)+'_'+str(y.device)], spec)
    spec = spectral_normalize_torch(spec)


    return spec


def get_dataset_filelist(wavs_dir):
    file_list = [os.path.join(wavs_dir, file_name) for file_name in os.listdir(wavs_dir)]
    return file_list





def collate_batch(batch):
    """Collate a batch of data."""
    # batch = batch[0]
    # spk_mels, input_mels, target_mels, word = zip(*batch)
    input_mels, target_mels, word = zip(*batch)
    # spk_mels = torch.stack(spk_mels)

    input_lens = [min(len(input_mel),300) for input_mel in input_mels]
    target_lens = [min(len(target_mel),300) for target_mel in target_mels]

    overlap_lens = input_lens

    input_mels = pad_sequence(input_mels, batch_first=True)  # (batch, max_src_len, wav2vec_dim)
    input_masks = [torch.arange(input_mels.size(1)) >= input_len for input_len in input_lens]
    input_masks = torch.stack(input_masks)  # (batch, max_src_len)

    target_mels = pad_sequence(target_mels, batch_first=True)
    # target_masks = [torch.arange(target_mels.size(1)) >= target_len for target_len in target_lens]
    # target_masks = torch.stack(target_masks)  # (batch, max_tgt_len)

    # input_mels = input_mels.unsqueeze(1)
    # input_masks = input_masks.unsqueeze(1)
    # target_mels = target_mels.unsqueeze(1)

    # return spk_mels, input_mels, input_masks, target_mels, word, overlap_lens
    return input_mels, input_masks, target_mels, word, overlap_lens

class MelDataset(torch.utils.data.Dataset):
    def __init__(self, training_files, n_fft, num_mels,
                 hop_size, win_size, sampling_rate,  fmin, fmax,device=None):
        self.audio_files = training_files
        random.seed(1234)
        random.shuffle(self.audio_files)

        self.sampling_rate = sampling_rate

        self.n_fft = n_fft
        self.num_mels = num_mels
        self.hop_size = hop_size
        self.win_size = win_size
        self.fmin = fmin
        self.fmax = fmax

        self.device = device


    def __getitem__(self, index):
        filename = self.audio_files[index]
        file_label = os.path.basename(filename).split(".")[0]
        audio,sampling_rate = load_wav(filename)


        ### split
        # if audio.size >= self.segment_size:
        #     max_audio_start = audio.size - self.segment_size
        #     audio_start = random.randint(0, max_audio_start)
        #     audio = audio[audio_start:audio_start + self.segment_size]
        #     file_label = file_label+"seg"+str(audio_start)
        # else:
        #     # audio = torch.nn.functional.pad(audio, (self.segment_size - audio.size), 'constant')
        #     audio = np.pad(audio, ((0,self.segment_size - audio.size)), 'constant')
        #     file_label = file_label + "seg0"


        # pitch_shift
        shift = random.choice(pitch_shift_list)
        audio_pitch = pyrb.pitch_shift(audio, sampling_rate, shift)
        file_label = file_label + "shift"+str(shift)
        # # audio = audio / MAX_WAV_VALUE
        audio = normalize(audio) * 0.95
        audio = torch.FloatTensor(audio)
        audio = audio.unsqueeze(0)
        #
        # # audio_pitch = audio_pitch / MAX_WAV_VALUE
        audio_pitch = normalize(audio_pitch) * 0.95
        audio_pitch = torch.FloatTensor(audio_pitch)
        audio_pitch = audio_pitch.unsqueeze(0)

        mel = mel_spectrogram(audio, self.n_fft, self.num_mels,
                              self.sampling_rate, self.hop_size, self.win_size, self.fmin, self.fmax,
                              center=False)
        mel_pitch = mel_spectrogram(audio_pitch, self.n_fft, self.num_mels,
                              self.sampling_rate, self.hop_size, self.win_size, self.fmin, self.fmax,
                              center=False)

        mel = mel.squeeze(0).transpose(0,1)
        mel_pitch = mel_pitch.squeeze(0).transpose(0,1)

        mel = mel_normalize(mel)
        mel_pitch = mel_normalize(mel_pitch)

        return mel_pitch, mel,file_label
        # return (mel, mel,file_label)


    def __len__(self):
        return len(self.audio_files)


class Test_MelDataset(torch.utils.data.Dataset):
    def __init__(self, test_files, n_fft, num_mels,
                 hop_size, win_size, sampling_rate,  fmin, fmax,device=None):
        self.audio_files = test_files


        self.sampling_rate = sampling_rate

        self.n_fft = n_fft
        self.num_mels = num_mels
        self.hop_size = hop_size
        self.win_size = win_size
        self.fmin = fmin
        self.fmax = fmax
        self.device = device


    def __getitem__(self, index):
        filename = self.audio_files[index]
        file_label = os.path.basename(filename).split(".")[0]
        audio,sampling_rate = load_wav(filename)
        ### split
        audio = normalize(audio) * 0.95
        audio = torch.FloatTensor(audio)
        audio = audio.unsqueeze(0)

        mel = mel_spectrogram(audio, self.n_fft, self.num_mels,
                              self.sampling_rate, self.hop_size, self.win_size, self.fmin, self.fmax,
                              center=False)
        mel = mel.squeeze(0).transpose(0,1)
        mel = mel_normalize(mel)
        return (mel,file_label)


    def __len__(self):
        return len(self.audio_files)



