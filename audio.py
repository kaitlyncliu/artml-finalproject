import whisper

import queue
import soundfile as sf
import sounddevice as sd

import pyttsx3

from gtts import gTTS
import os

CHANNELS = 1
FS = 44100 # sample rate (double the max human frequency)

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(indata.copy())

def stt():
    try:
        with sf.SoundFile("recording.wav", mode='w', samplerate=FS, 
                            channels=CHANNELS) as file:
            with sd.InputStream(samplerate=FS, channels=CHANNELS, callback=callback):
                print('#' * 80)
                print('Press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())

    except KeyboardInterrupt:
        print("Ctrl+C pressed!")
    except Exception as e:
        print("Exited! {}".format(e))
        exit()

    model = whisper.load_model("small")
    result = model.transcribe("recording.wav")

    file = open("recording.txt", "w")
    file.write(result["text"])
    print(result["text"])
    file.close()

DO_GOOGLE = True

def tts():
    file = open("recording.txt", 'r')
    text = file.read().replace('\n', '')

    if not DO_GOOGLE:
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[14].id)

        engine.say(text)
        engine.runAndWait()

    else:
        gttsObj = gTTS(text=text, lang='en', tld='ca', slow=False)
        gttsObj.save("gemini_response.mp3")
        os.system("afplay gemini_response.mp3")

    file.close()

def main():
    stt()
    tts()

if __name__ == "__main__":
    main()