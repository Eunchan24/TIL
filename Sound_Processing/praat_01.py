#import moviepy.editor as mp
import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

import plotly.graph_objects as go

# clip = mp.VideoFileClip('C:\\Users\\USER\\Downloads\\present.mp4')
# clip.audio.write_audiofile('C:\\Users\\USER\\Downloads\\audio.wav')

audio_path = '/Users/eunchankim/Desktop/prosodic-analysis-master/wavs/qwe.wav'
file = audio_path.split('/')[4]

pitch_values = []
pitch_ceiling = 400   # In Hz, change according to gender
pitch_floor = 50    # In Hz, change according to gender
smooth_bandwidth = 5



def load_wave(filepath):
    waveform = parselmouth.Sound(filepath)
    waveform = parselmouth.praat.call(waveform, "Convert to mono")
    return waveform

def extract_pitch(waveform):
    #print(waveform.to_pitch())
    return waveform.to_pitch(pitch_ceiling=pitch_ceiling, pitch_floor=pitch_floor)
def set_pitch_analysis(pitch_analysis):
    # Array with fundamental frequency values
    pitch_countour = pitch_analysis.selected_array['frequency']
    pitch_countour[pitch_countour == 0] = np.nan
    pitch_values.append(pitch_countour)
    # Interpolated contour
    interpolated = pitch_analysis.interpolate().selected_array['frequency']
    interpolated[interpolated == 0] = np.nan
    # Smoothed version
    smoothed = pitch_analysis.smooth(bandwidth=smooth_bandwidth).selected_array['frequency']
    smoothed[smoothed == 0] = np.nan
    draw_pitch(pitch_countour, smoothed, interpolated, pitch_analysis.xs())

def draw_pitch(pitch, smoothed, interpolated, xaxis):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xaxis[1:],
        y=interpolated,
        name="interpolated",
        line=dict(color='Gray', width=1.5)
    )
    )
    print(np.nanmean(interpolated))
    print(np.nanmean(smoothed))
    print(np.nanmean(pitch))
    print(np.nanstd(pitch))
    #fig.write_image("fig1.png")
    fig.show()


set_pitch_analysis(extract_pitch(load_wave(audio_path)))