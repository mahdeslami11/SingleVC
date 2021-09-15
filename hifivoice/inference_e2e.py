from __future__ import absolute_import, division, print_function, unicode_literals

import glob
import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import sys
sys.path.append("/home/gyw/workspace/program/VC/SingleVC/")
sys.path.append("../")

import numpy as np
import argparse
import json
import torch
from scipy.io.wavfile import write
from hifivoice.env import AttrDict
from hifivoice.meldataset import MAX_WAV_VALUE
from hifivoice.models import Generator

h = None
device = None


def load_checkpoint(filepath, device):
    assert os.path.isfile(filepath)
    print("Loading '{}'".format(filepath))
    checkpoint_dict = torch.load(filepath, map_location=device)
    print("Complete.")
    return checkpoint_dict


def scan_checkpoint(cp_dir, prefix):
    pattern = os.path.join(cp_dir, prefix + '*')
    cp_list = glob.glob(pattern)
    if len(cp_list) == 0:
        return ''
    return sorted(cp_list)[-1]


def inference(a,h):
    checkpoint_file = r"/home/gyw/workspace/program/VC/SingleVC/hifivoice/pretrained/UNIVERSAL_V1/g_02500000"


    generator = Generator(h).to(device)

    state_dict_g = load_checkpoint(checkpoint_file, device)
    generator.load_state_dict(state_dict_g['generator'])

    # filelist = os.listdir(a.input_mels_dir)

    #os.makedirs(output_dir, exist_ok=True)

    generator.eval()
    generator.remove_weight_norm()
    with torch.no_grad():
        for file_name, input_mel in a.input_mels_list:
            # file_path = os.path.join(a.input_mels_dir, filname)
            # file_path = os.path.join(a.input_mels_dir, filname)
            # x = np.load(file_path)
            x = input_mel
            x = torch.FloatTensor(x).to(device)
            y_g_hat = generator(x)
            audio = y_g_hat.squeeze()
            # audio = audio * MAX_WAV_VALUE
            # audio = audio.cpu().numpy().astype('int16')
            audio = audio.cpu().numpy()

            output_file = os.path.join(a.output_dir, file_name + '_generated_e2e.wav')
            write(output_file, h.sampling_rate, audio)
            print(output_file)


# def hifi_infer(input_mels_dir,output_dir):
def hifi_infer(input_mels_list,output_dir):
    print('Initializing Inference Process..')

    parser = argparse.ArgumentParser()
    # parser.add_argument('--input_mels_dir', default='')
    parser.add_argument('--input_mels_list', type=str, nargs="+",default="")
    parser.add_argument('--output_dir', default='')
    parser.add_argument('--checkpoint_file', default="/home/gyw/workspace/program/VC/SingleVC/hifivoice/pretrained/UNIVERSAL_V1/config.json")
    a = parser.parse_args()

    # a.input_mels_dir = input_mels_dir
    a.input_mels_list = input_mels_list
    a.output_dir = output_dir

    config_file = os.path.join(os.path.split(a.checkpoint_file)[0], 'config.json')

    with open(config_file) as f:
        data = f.read()

    global h
    json_config = json.loads(data)
    h = AttrDict(json_config)

    torch.manual_seed(h.seed)
    global device
    if torch.cuda.is_available():
        torch.cuda.manual_seed(h.seed)
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    inference(a,h)


# if __name__ == '__main__':
#     main()

