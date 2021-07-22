# Vietnamese Text to Speech

- Forward Tacotron trained Vietnamese Dataset.
- This work is heavily based on [ForwardTacotron](https://github.com/as-ideas/ForwardTacotron). For a more detailed description, please see the original authors [README](!https://github.com/as-ideas/ForwardTacotron/blob/master/README.md).

## Dataset:
- [Zalo VLSP 2019](https://vlsp.org.vn/sites/default/files/2019-10/VLSP2019-TTS-PhungVietLam.pdf)

## Installation
- Python >= 3.6
- Install dependencies:
```
pip install -r requirements.txt
```

## Demo:
- Run the notebook `demo.ipynb` or run the following script:
```
python demo.py --text "Nhập một đoạn văn bản bất kì" --output model_outputs
```

## Pretrained models:
Can be found in `pretrained` directory:
- `tacotron_89K.pyt`: pretrained model for Tacotron
- `forward_300K.pyt`: pretrained model for Forward Tacotron
- `model_loss0.028723_step860000_weights.pyt`: pretrained model for WaveRNN

## Training:

(1) Preprocess the dataset:
 ```
python preprocess.py --path /path/to/dataset
```
(2) Train Tacotron with:
```
python train_tacotron.py
```
(3) Use the trained tacotron model to create alignment features with:
```
python train_tacotron.py --force_align
```
(4) Train ForwardTacotron with:
```
python train_forward.py
```

For training the model, just bring it to the [LJSpeech](https://keithito.com/LJ-Speech-Dataset/) format:
```
|- dataset_folder/
|   |- metadata.csv
|   |- wav/
|       |- file1.wav
|       |- ...
```

Or refer to the original repo [ForwardTacotron](https://github.com/as-ideas/ForwardTacotron) for more in depth details.