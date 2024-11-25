import torch
import torch.nn as nn
from transformers import Wav2Vec2Processor
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os
import librosa
import numpy as np


class RegressionHead(nn.Module):
    r"""Classification head."""

    def __init__(self, config):
        super().__init__()

        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.dropout = nn.Dropout(config.final_dropout)
        self.out_proj = nn.Linear(config.hidden_size, config.num_labels)

    def forward(self, features, **kwargs):
        x = features
        x = self.dropout(x)
        x = self.dense(x)
        x = torch.tanh(x)
        x = self.dropout(x)
        x = self.out_proj(x)

        return x


class EmotionModel(nn.Module):
    r"""Speech emotion classifier."""

    def __init__(self):
        super().__init__()
        # Initialize emotion2vec pipeline
        self.emotion_pipeline = pipeline(
            task=Tasks.emotion_recognition,
            model="iic/emotion2vec_plus_large"
        )

    def forward(self, file_path):
        # Directly use file path as input for emotion2vec
        outputs = self.emotion_pipeline(file_path, granularity="utterance", extract_embedding=True)
        embedding = outputs[0]['feats']  # Extract the embedding
        return torch.tensor(embedding).unsqueeze(0)


# Instantiate the model
device = 'cuda' if torch.cuda.is_available() else "cpu"
emotion_model = EmotionModel().to(device)


def process_func(
        file_path: str,
        embeddings: bool = False,
) -> np.ndarray:
    r"""Predict emotions or extract embeddings from audio file."""

    # run through model
    with torch.no_grad():
        embedding = emotion_model(file_path)

    # convert to numpy
    return embedding.detach().cpu().numpy()


def extract_dir(path):
    embs = []
    wavnames = []
    for idx, wavname in enumerate(os.listdir(path)):
        file_path = os.path.join(path, wavname)
        if not wavname.endswith(".wav"):
            continue
        emb = process_func(file_path, embeddings=True)
        embs.append(emb)
        wavnames.append(wavname)
        np.save(f"{file_path}.emo.npy", emb.squeeze(0))
        print(idx, wavname)


def extract_wav(file_path):
    emb = process_func(file_path, embeddings=True)
    return emb


def preprocess_one(file_path):
    emb = process_func(file_path, embeddings=True)
    np.save(f"{file_path}.emo.npy", emb.squeeze(0))
    return emb


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Emotion Extraction Preprocess')
    parser.add_argument('--filelists', dest='filelists', nargs="+", type=str, help='path of the filelists')
    args = parser.parse_args()

    for filelist in args.filelists:
        print(filelist, "----start emotion extract-------")
        with open(filelist) as f:
            for idx, line in enumerate(f.readlines()):
                file_path = line.strip().split("|")[0]
                preprocess_one(file_path)
                print(idx, file_path)
