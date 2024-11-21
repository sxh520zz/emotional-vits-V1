import os
import librosa
import tqdm
import soundfile as sf
import time
 
if __name__ == '__main__':
 
    audioExt = 'WAV'
 
    input_sample = 22050
 
    output_sample = 16000
 
 
    audioDirectory = ['/media/shixiaohan-toda/70e9f22b-13a4-429e-acad-a8786e1f1143/DataBase/LJSpeech-1.1/wavs/']
 
 
    outputDirectory = ['/home/shixiaohan-toda/Desktop/Conferences/Interspeech_2025_EMO_TTS/emotional-vits-main/DUMMY1/']
 
    start_time=time.time()
 
    for i, dire in enumerate(audioDirectory):
 
        clean_speech_paths = librosa.util.find_files(
                directory=dire,
                ext=audioExt,
                recurse=True, 
            )
 
        for file in tqdm.tqdm(clean_speech_paths, desc='No.{} dataset resampling'.format(i)):
 
            fileName = os.path.basename(file)
 
            y, sr = librosa.load(file, sr=input_sample)
 
            y_16k = librosa.resample(y, orig_sr=sr, target_sr=output_sample)
   
            outputFileName = os.path.join(outputDirectory[i], fileName)
  
            sf.write(outputFileName, y_16k, output_sample)
        end_time=time.time()
        runTime=end_time - start_time
        print("Run Time: {} sec ~".format(runTime))