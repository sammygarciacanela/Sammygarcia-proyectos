# Herramientas de edición

`transcribir.py` pasa a texto el audio de un video, con el tiempo de cada palabra. Usa el modelo Whisper.

```bash
pip install faster-whisper
ffmpeg -i video.MOV -vn -ac 1 -ar 16000 audio.wav
python3 transcribir.py audio.wav medium   # genera audio.wav.json
```
