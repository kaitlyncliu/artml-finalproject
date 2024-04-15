import whisper

import queue
import soundfile as sf
import sounddevice as sd

CHANNELS = 1
FS = 44100 # sample rate (double the max human frequency)
DURATION = 3

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(indata.copy())

def main():
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

if __name__ == "__main__":
    main()