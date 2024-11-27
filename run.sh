#!/bin/bash
#SBATCH -n 1 # 指定核心数量
#SBATCH -N 1 # 指定node的数量
#SBATCH --gres=gpu:1 # 需要使用多少GPU，n是需要的数量
#SBATCH --exclude mrcompute01,compute02,compute01,compute04,compute05,compute06
#SBATCH -t 7-00:00:00


#nohup python -u train.py > 1.log 2>&1 &

#python train_ms.py -c configs/shi.json -m shi --ckptD /home/Shi22/nas01home/TTS_EMO/emotional-vits-main-ESD-E2V/D_680000.pth --ckptG /home/Shi22/nas01home/TTS_EMO/emotional-vits-main-ESD-E2V/G_680000.pth
#python train_ms.py -c configs/shi.json -m shi
python -u emotion_extract.py --filelists filelists/updated_test.txt 
#python -u emotion_extract.py --filelists /home/Shi22/nas01home/TTS_EMO/emotional-vits-main-ESD/filelists/train.txt /home/Shi22/nas01home/TTS_EMO/emotional-vits-main-ESD/filelists/val.txt