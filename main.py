
# run with: python main.py no_type.wav
import pyaudio
import wave
import time
import sys
import strip_worker

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# Create strip thread
worker = strip_worker.StripWorker("Light Strip Worker")
worker.start()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    worker.addFrame(data)

    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
try:
    while stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt:
    worker.stop()


# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# stop thread
worker.stop()
worker.join()

# close PyAudio (7)
p.terminate()
