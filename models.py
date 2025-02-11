import urllib.request
import tarfile
import shutil
import os

#func to download
def download_requireq_models(url, filepath):
    try:
        urllib.request.urlretrieve(url, filepath)
    except Exception as e:
        print(e);

def extract_tar(filePath):
    try:
        tar = tarfile.open(filePath, "r:gz");
        tar.extractall()
        tar.close()
    except Exception as e:
        print(e)

download_requireq_models("https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz", "piper_arm64.tar.gz");     
download_requireq_models("https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx?download=true", "voice.onnx")
download_requireq_models("https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx?download=true", "voice.onnx.json")
extract_tar("piper_arm64.tar.gz")
shutil.move('voice.onnx', "piper/voice.onnx")
shutil.move('voice.onnx.json', "piper/voice.onnx.json")
shutil.copyfile("raspi-assistant.py", "piper/raspi-assistant.py")

#remove
os.remove("piper_arm64.tar.gz")