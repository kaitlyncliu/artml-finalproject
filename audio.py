import whisper

import queue
import soundfile as sf
import sounddevice as sd
from pynput import keyboard

from gtts import gTTS
import os

from speechbrain.inference.interfaces import foreign_class

classifier = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP", 
                           pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")

# Spacebar press exception to help with debugging
class SpaceException(Exception):
    pass

CHANNELS = 1
FS = 44100 # sample rate (double the max human frequency)

q = queue.Queue()

# handles the key presses from the Listener thread and kills it if the spacebar
# pressed
def on_press(key):
    if (key == keyboard.Key.space):
        return False

# handles the periodic storage of audio from the InputStream thread
def callback(indata, frames, time, status):
    q.put(indata.copy())

# Opens a .wav file and spawns two threads to handle recording audio and monitoring
# keystrokes. Once the spacebar has been pressed, the InputStream stops recording
# audio and loads the .wav file into OpenAI's whisper model. Once Whisper has finished,
# the text is stored in a .txt file to be used by the backend.
def speech2text():
    try:
        with sf.SoundFile("recording.wav", mode='w', samplerate=FS, 
                            channels=CHANNELS) as f:
            with sd.InputStream(samplerate=FS, channels=CHANNELS, callback=callback):
                with keyboard.Listener(on_press=on_press) as l:
                    print('#' * 80)
                    print('Press the spacebar to stop the recording')
                    print('#' * 80)
                    while True:
                        f.write(q.get())
                        if not l.is_alive():
                            raise SpaceException
    
    except SpaceException:
        print("Spacebar was pressed!")
    except KeyboardInterrupt:
        print("\nCtrl+C was pressed")
        exit()
    except Exception as e:
        print("Exited! {}".format(e))
        exit()

    model = whisper.load_model("small")
    result = model.transcribe("recording.wav")

    out_prob, score, index, tone = classifier.classify_file("recording.wav")

    file = open("outputrecording.txt", "w")
    file.write(tone[0] + '\n')
    file.write(result["text"])
    file.close()

# Opens a .txt file in the directory and reads it into a string. Then that string 
# is passed into Google's text-to-speech model which stores the audio in an .mp3
# file and read out on the speakers using an os.system call.
def text2speech():
    file = open("gemini_response.txt", 'r')
    text = file.read().replace('\n', '')

    gttsObj = gTTS(text=text, lang='en', tld='ca', slow=False)
    gttsObj.save("gemini_response.mp3")
    os.system("afplay gemini_response.mp3")

    file.close()

# def main():
    # something to handle button on gui and also sending recordings/text to db
    # for now just call both functions
    # speech2text()
    # text2speech()

# if __name__ == "__main__":
#     main()