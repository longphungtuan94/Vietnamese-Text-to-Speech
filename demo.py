from notebook_utils import synthesize
from utils import hparams as hp

import utils.text.cleaners as cleaners
from scipy.io import wavfile
import numpy as np
import string
import argparse

SAMPLE_RATE = 22050

parser = argparse.ArgumentParser()
parser.add_argument(
    '-t','--text', help='Input text',
    default='Đó là lần tôi ở Đà Lạt non một tháng làm nhiệm vụ nghiên cứu chính sách đất đai cho đồng bào dân tộc thiểu số Tây Nguyên cuối năm 2004'
)
parser.add_argument('-o', '--output', help='Directory to save output wave files', default='model_outputs')

args = parser.parse_args()


forward_model_path = 'pretrained/forward_300K.pyt'
voc_model_path = 'pretrained/model_loss0.028723_step860000_weights.pyt'

print('*** Configure hparams...')
synthesize.init_hparams('hparams.py')
print('*** Loading forward model')
forward_model = synthesize.get_forward_model(forward_model_path)
print('*** Loading VOC model')
voc_model = synthesize.get_wavernn_model(voc_model_path)

text = args.text

# Using WaveRNN vocoder
wav = synthesize.synthesize(text, forward_model, voc_model)
# Using Griffin-Lim vocoder
gl_wav = synthesize.synthesize(text, forward_model, 'griffinlim')

# Write the audio using WaveRNN vocoder
wavfile.write('{}/wavernn.wav'.format(args.output), SAMPLE_RATE, wav)
# Write the audio using Griffin-Lim vocoder
wavfile.write('{}/griffinlim.wav'.format(args.output), SAMPLE_RATE, gl_wav)