"""
https://github.com/suno-ai/bark?tab=readme-ov-file#-installation
"""

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from pydub import AudioSegment
import numpy as np
import nltk
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)
silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence


def increase_speed(input_file, output_file, speed_factor):
    # Load the audio file
    sound = AudioSegment.from_wav(input_file)

    # Calculate the new duration after increasing speed
    new_duration = int(len(sound) / speed_factor)

    # Increase the speed
    sped_up_sound = sound.speedup(playback_speed=speed_factor)

    # Trim or pad the audio to match the new duration
    if len(sped_up_sound) > new_duration:
        sped_up_sound = sped_up_sound[:new_duration]
    elif len(sped_up_sound) < new_duration:
        sped_up_sound += AudioSegment.silent(duration=new_duration - len(sped_up_sound))

    # Export the modified audio to a new WAV file
    sped_up_sound.export(output_file, format="wav")


# download and load all models
preload_models()
speakers = [
    "v2/en_speaker_0",
    "v2/en_speaker_1",
    "v2/en_speaker_2",
    "v2/en_speaker_3",
    "v2/en_speaker_4",
    "v2/en_speaker_5",  # noisy
    "v2/en_speaker_6",
    "v2/en_speaker_7",
    "v2/en_speaker_8",
    "v2/en_speaker_9",
]
voices = {"Nova:": "v2/en_speaker_9", "Mr.Catty:": "v2/en_speaker_8"}

## Non speech sounds
# [laughter]
# [laughs]
# [sighs]
# [music]
# [gasps]
# [clears throat]
# — or ... for hesitations
# ♪ for song lyrics

text_prompt = """Mr. Catty: I want to learn this concept really fast, but it's a 30-minute YouTube video. What do I do?
Mr. Catty: I don't like writing long emails and reports.
Mr.Catty: [sighs] I'm tired of spending hours filling out repetitive content in my 560 interview applications.
Mr. Catty: Sometimes, I come need to extract text out of an image. It's such a hassle.
"""
sentences = nltk.sent_tokenize(text_prompt)

pieces = []
previous_speaker = "ubNKNOWN"
for sentence in sentences:
    sentence = sentence.lstrip()
    if not sentence:
        continue
    if sentence.startswith("Nova:"):
        sentence = sentence.lstrip("Nova:")
        sentence = sentence.lstrip()
        print(f"Nova: {sentence}")
        speaker = "Nova:"
    elif sentence.startswith("Mr. Catty:") or sentence.startswith("Mr.Catty:"):
        sentence = sentence.lstrip("Mr.Catty:")
        sentence = sentence.lstrip("Mr. Catty:")
        sentence = sentence.lstrip()
        print(f"Mr. Catty: {sentence}")
        speaker = "Mr.Catty:"
    else:
        print(f"{previous_speaker}: {sentence}")
    audio_array = generate_audio(sentence, history_prompt=voices[speaker])
    pieces += [audio_array]
    previous_speaker = speaker


write_wav(f"regular_speed.wav", SAMPLE_RATE, np.concatenate(pieces))
print("Making the audio faster...")
increase_speed("regular_speed.wav", "fast.wav", 1.5)
print("done")
