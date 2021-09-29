import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
# import sys
# sys.path.append("")
import numpy as np
import time
import yaml
import torch
from torch.backends import cudnn
from torch.utils.data import DataLoader
from any2one import util
from any2one.meldataset import MelDataset, Test_MelDataset, get_dataset_filelist,collate_batch,mel_denormalize
from any2one.model.any2one import Generator
from hifivoice.inference_e2e import  hifi_infer

class Solver():
	def __init__(self, config):
		super(Solver, self).__init__()
		self.config = config
		self.local_rank = self.config['local_rank']
		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
		self.make_records()
		# train parameters
		self.total_epochs = self.config['epochs']
		self.save_period = self.config['save_period']
		self.eval_period = self.config['eval_period']
		self.step_record_time = self.config['step_record_time']
		self.learning_rate = self.config["learning_rate"]
		# training model
		self.Generator = Generator().to(self.device)
		self.optimizer = torch.optim.AdamW(
			[{'params': self.Generator.parameters(), 'initial_lr': self.config["learning_rate"]}],
			self.config["learning_rate"],betas=[self.config["adam_b1"], self.config["adam_b2"]])
		self.scheduler = torch.optim.lr_scheduler.ExponentialLR(self.optimizer, gamma=self.config["lr_decay"])
		
		self.criterion = torch.nn.L1Loss()
		self.init_epoch = 0
		if self.config['resume']:
			self.resume_model(self.config['resume_model_path'])
		self.logging.info('config = %s', self.config)
		self.logging.info('param Generator size = %fM',util.count_parameters_in_M(self.Generator))


	def make_records(self):
		time_record = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
		self.log_dir = os.path.join(self.config['out_dir'],time_record,"log")
		self.model_dir = os.path.join(self.config['out_dir'],time_record,"model")
		self.write_dir = os.path.join(self.config['out_dir'],time_record,"write")
		self.convt_mel_dir = os.path.join(self.config['out_dir'],time_record,"infer","mel")
		self.convt_voice_dir = os.path.join(self.config['out_dir'],time_record,"infer","voice")

		os.makedirs(self.log_dir, exist_ok=True)
		os.makedirs(self.model_dir, exist_ok=True)
		os.makedirs(self.write_dir, exist_ok=True)
		os.makedirs(self.convt_mel_dir, exist_ok=True)
		os.makedirs(self.convt_voice_dir, exist_ok=True)

		self.logging = util.Logger(self.log_dir, "log.txt")
		self.writer = util.Writer(self.write_dir)

	def get_train_data_loaders(self):
		train_filelist = get_dataset_filelist(self.config["train_wav_dir"])
		trainset = MelDataset(train_filelist, self.config["n_fft"],self.config["num_mels"],
							  self.config["hop_size"], self.config["win_size"], self.config["sampling_rate"],self.config["fmin"],
							  self.config["fmax"],device=self.device)
		self.train_data_loader = DataLoader(trainset, num_workers=self.config["num_workers"], shuffle=True, sampler=None,
									   batch_size=self.config["batch_size"], collate_fn=collate_batch,pin_memory=False, drop_last=True)

	def get_test_data_loaders(self):
		test_filelist = get_dataset_filelist(self.config["test_wav_dir"])
		testset = Test_MelDataset(test_filelist, self.config["n_fft"],self.config["num_mels"],
							 self.config["hop_size"], self.config["win_size"], self.config["sampling_rate"],self.config["fmin"],
							 self.config["fmax"], device=self.device)
		test_data_loader = DataLoader(testset, num_workers=1, shuffle=False, sampler=None,
									  batch_size=1, pin_memory=False, drop_last=True)
		return test_data_loader
	
	def resume_model(self, resume_model_path):
		self.logging.info('【loading the model】 from %s' % (resume_model_path))
		checkpoint = torch.load(resume_model_path, map_location='cpu')
		# start epoch
		self.init_epoch = checkpoint['epoch']
		self.Generator.load_state_dict(checkpoint['Generator'])
		self.optimizer.load_state_dict(checkpoint['optimizer'])
		self.scheduler.load_state_dict(checkpoint['scheduler'])

	def reset_grad(self):
		self.optimizer.zero_grad()

	def train(self):
		self.Generator.train()
		for epoch in range(self.init_epoch, self.total_epochs):
			# produce random pitch shifts
			self.get_train_data_loaders()
			self.len_train_data = len(self.train_data_loader)
			self.logging.info('************************************   train epoch %d ****************************',epoch)
			lr = self.optimizer.state_dict()['param_groups'][0]['lr']
			self.logging.info('【train %d】lr:  %.10f', epoch, lr)
			for step, (input_mels, input_masks, target_mels, word, overlap_lens) in enumerate(self.train_data_loader):
				input_mels = input_mels.cuda()
				target_mels = target_mels.cuda()
				input_masks = input_masks.cuda()
				fake_mels = self.Generator(input_mels,input_masks)
				losses = []
				for fake_mel, target_mel, overlap_len in zip(fake_mels.unbind(), target_mels.unbind(), overlap_lens):
					temp_loss = self.criterion(fake_mel[:overlap_len, :], target_mel[:overlap_len, :])
					losses.append(temp_loss)
				loss = sum(losses) / len(losses)
				self.reset_grad()
				loss.backward()
				self.optimizer.step()

				total_step = step + epoch * self.len_train_data
				if total_step % self.step_record_time == 0:
					self.writer.add_scalar('train/lr', lr, total_step)
					self.writer.add_scalar('train/loss' , loss, total_step)
					self.logging.info('【train_%d】 %s:  %f ', step, word[0], loss)

			if epoch % self.save_period == 0 or epoch == (self.total_epochs - 1):
				save_model_path = os.path.join(self.model_dir,'checkpoint-%d.pt' % (epoch))
				self.logging.info('saving the model to the path:%s',save_model_path)
				torch.save({'epoch': epoch + 1,
						'config': self.config,
						'Generator': self.Generator.state_dict(),
						'optimizer': self.optimizer.state_dict(),
						'scheduler': self.scheduler.state_dict()},
						save_model_path, _use_new_zipfile_serialization=False)
				# infer
				self.infer(epoch)
				self.scheduler.step()
		self.writer.close()
	
	def infer(self,epoch):
		test_data_loader = self.get_test_data_loaders()
		self.Generator.eval()
		mel_npy_file_list=[]
		with torch.no_grad():
			for idx, (input_mel, word) in enumerate(test_data_loader):
				input_mel = input_mel.cuda()
				fake_mel = self.Generator(input_mel,None)
				fake_mel = torch.clamp(fake_mel, min=0, max=1)
				fake_mel = mel_denormalize(fake_mel)
				fake_mel = fake_mel.transpose(1,2)
				fake_mel = fake_mel.detach().cpu().numpy()
				file_name = "epoch"+str(epoch)+"_"+word[0]
				mel_npy_file = os.path.join(self.convt_mel_dir, file_name+ '.npy')
				np.save(mel_npy_file, fake_mel, allow_pickle=False)
				mel_npy_file_list.append([file_name,fake_mel])
		hifi_infer(mel_npy_file_list,self.convt_voice_dir,self.config["hifi_model_path"],self.config["hifi_config_path"])
		self.Generator.train()
		


if __name__ == '__main__':
	cudnn.benchmark = True
	config_path = r"any2one/config.yaml"
	with open(config_path) as f:
		config = yaml.load(f, Loader=yaml.Loader)
	solver = Solver(config)
	solver.train()