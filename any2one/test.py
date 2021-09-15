import wave

import contextlib

fname = '/home/gyw/workspace/program/VC/GAE-VC/cuda1/output/voc_output/__p230_003__797k_steps_gen_batched_target11000_overlap550.wav'


f = wave.open(fname, 'r')
frames = f.getnframes()

rate = f.getframerate()

duration = frames / float(rate)
duration = float('%.2f' % duration)
print(duration)
