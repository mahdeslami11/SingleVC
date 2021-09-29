import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
# import sys
# sys.path.append("/home/gyw/workspace/program/VC/SingleVC_G")
import torch
from torch.backends import cudnn
from torch.utils.data import DataLoader
import numpy as np
import yaml
import time
from any2one import util
from any2one.meldataset import Test_MelDataset, get_dataset_filelist,mel_denormalize
from any2one.model.any2one import Generator
from hifivoice.inference_e2e import  hifi_infer

class Solver():
	def __init__(self, config):
		super(Solver, self).__init__()
		self.config = config
		self.local_rank = self.config['local_rank']
		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
		self.make_records()
		self.Generator = Generator().to(self.device)
		self.init_epoch = 0
		if self.config['resume']:
			self.resume_model(self.config['resume_model_path'])
		self.logging.info('config = %s', self.config)
		print('param Generator size = %fM ' % (util.count_parameters_in_M(self.Generator)))

	def make_records(self):
		time_record = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
		self.log_dir = os.path.join(self.config['out_dir'], time_record, "log")
		self.convt_mel_dir = os.path.join(self.config['out_dir'], time_record, "infer", "mel")
		self.convt_voice_dir = os.path.join(self.config['out_dir'], time_record, "infer", "voice")
		os.makedirs(self.log_dir, exist_ok=True)
		os.makedirs(self.convt_mel_dir, exist_ok=True)
		os.makedirs(self.convt_voice_dir, exist_ok=True)
		self.logging = util.Logger(self.log_dir, "log.txt")

	def get_test_data_loaders(self):
		test_filelist = get_dataset_filelist(self.config["test_wav_dir"])
		testset = Test_MelDataset(test_filelist, self.config["n_fft"],self.config["num_mels"],
							 self.config["hop_size"], self.config["win_size"], self.config["sampling_rate"],self.config["fmin"],
							 self.config["fmax"], device=self.device)
		test_data_loader = DataLoader(testset, num_workers=1, shuffle=False, sampler=None,
									  batch_size=1, pin_memory=False, drop_last=True)
		return test_data_loader

	def resume_model(self, resume_model_path):
		checkpoint_file = resume_model_path
		self.logging.info('loading the model from %s' % (checkpoint_file))
		checkpoint = torch.load(checkpoint_file, map_location='cpu')
		self.init_epoch = checkpoint['epoch']
		self.Generator.load_state_dict(checkpoint['Generator'])

	def infer(self):
		# infer  prepare
		test_data_loader = self.get_test_data_loaders()
		self.Generator.eval()
		self.Generator.remove_weight_norm()
		mel_npy_file_list=[]
		with torch.no_grad():
			for idx, (input_mel, word) in enumerate(test_data_loader):
				input_mel = input_mel.cuda()
				fake_mel = self.Generator(input_mel,None)
				fake_mel = torch.clamp(fake_mel, min=0, max=1)
				fake_mel = mel_denormalize(fake_mel)
				fake_mel = fake_mel.transpose(1,2)
				fake_mel = fake_mel.detach().cpu().numpy()
				file_name = "epoch"+"_"+word[0]
				mel_npy_file = os.path.join(self.convt_mel_dir, file_name+ '.npy')
				np.save(mel_npy_file, fake_mel, allow_pickle=False)
				mel_npy_file_list.append([file_name,fake_mel])
				if len(mel_npy_file_list)==500 or idx == len(test_data_loader)-1:
					self.logging.info('【infer_%d】 len: %d', idx,len(mel_npy_file_list))
					hifi_infer(mel_npy_file_list, self.convt_voice_dir,self.config["hifi_model_path"],self.config["hifi_config_path"])
					mel_npy_file_list.clear()

if __name__ == '__main__':
	cudnn.benchmark = True
	config_path = r"infer/infer_config.yaml"
	with open(config_path) as f:
		config = yaml.load(f, Loader=yaml.Loader)
	solver = Solver(config)
	solver.infer()