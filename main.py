
# run with: python main.py no_type.wav
import pyaudio
import wave
import time
import sys
import strip_worker
import numpy as np

SAMPLES_PER_WINDOW = 512

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

print(sys.argv[1])
wf = wave.open(sys.argv[1], 'rb')

wf.getsampwidth()

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# Create strip thread
worker = strip_worker.StripWorker(SAMPLES_PER_WINDOW, wf.getframerate(), "Light Strip Worker")
worker.start()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    assert frame_count <= SAMPLES_PER_WINDOW
    data = wf.readframes(frame_count)
    dtype = np.dtype('u'+str(wf.getsampwidth()))
    samps = np.fromstring(data, dtype)
    chans = np.reshape(samps, (2, -1), 'F').astype(np.float)
    worker.addWindow(chans)

    return (samps.tobytes(), pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback,
                frames_per_buffer=SAMPLES_PER_WINDOW)

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

p.terminate()
# stop thread
worker.stop()
worker.join()

# close PyAudio (7)
p.terminate()
