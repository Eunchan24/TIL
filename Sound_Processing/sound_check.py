import numpy as np
import parselmouth
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 음성 분석 클래스 입니다. by.동건,은찬
class Sound_Check:

    # 초기값으로 wav파일과 성별을 입력받습니다. by.동건,은찬
    def __init__(self, filepath, sex):
        self.filepath = filepath
        self.sex = sex

    # wav 데이터를 받고 waveform(파형)데이터로 변환 by.동건,은찬
    def load_wave(self):
        waveform = parselmouth.Sound(self.filepath)
        waveform = parselmouth.praat.call(waveform, "Convert to mono")
        return waveform

    # pitch의 max값과 min 값을 설정 by.동건,은찬
    def extract_pitch(self, waveform):
        pitch_analysis = waveform.to_pitch(pitch_ceiling=400, pitch_floor=50)
        return pitch_analysis

    # extract_pitch함수의 pitch를 받습니다. by.동건,은찬
    def set_pitch_analysis(self, pitch_analysis):
        # pitch 데이터 전처리 by.동건,은찬
        interpolated = pitch_analysis.interpolate().selected_array['frequency']
        interpolated[interpolated == 0] = np.nan

        # 전처리된 데이터를 분석 모델에 적용 by.동건,은찬
        self.sound_model(interpolated)
        # 전처리된 데이터로 x축:시간, y축:주파수(Hz)형태인 그래프를 생성하는 함수에 적용합니다. by.동건,은찬
        self.draw_pitch(interpolated, pitch_analysis.xs())

    # x축:시간, y축:주파수(Hz)형태인 그래프를 생성하는 함수입니다. by.동건,은찬
    def draw_pitch(self, interpolated, xaxis):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=xaxis[1:],
            y=interpolated,
            name="interpolated",
            line=dict(color='skyblue', width=1.5)
        ))
        fig.update_layout(template="plotly_white",
                          showlegend=True,
                          title="목소리의 높낮이 측정",
                          xaxis_title="시간(s)",
                          yaxis_title="HZ",
                          legend_title="The pitch of voice",
                          font=dict(
                              family="Courier New, monospace",
                              size=18,
                              color="Black"))

        #fig.write_image("fig1.png")

        fig.show()

    # pitch 분석 모델 입니다. by.동건,은찬
    def sound_model(self, interpolated):
        mean = int(round(np.nanmean(interpolated)))
        std = int(round(np.nanstd(interpolated)))

        print(mean)
        print(std)

        if self.sex == 'man':
            if std < 20:
                return print("너무 단조롭다")

            elif std >= 20 and std < 30:
                return print("무난하다")

            elif std >= 30 and std <= 55:
                return print("아나운서와 유사, good")

            elif std > 55:
                return print("너무 산만하거나, 너무 긴장한다.")

        elif self.sex == 'woman':
            if std < 45:
                return print("너무 단조롭다")

            elif std >= 45 and std < 55:
                return print("무난하다")

            elif std >= 55 and std <= 70:
                return print("아나운서와 유사, good")

            elif std > 70:
                return print("너무 산만하거나, 너무 긴장한다.")

# 메인 실행 함수 입니다. by.동건,은찬
if __name__ == '__main__':
    audio_path = '/Users/eunchankim/Downloads/man/man_2.wav'
    sex = 'man'
    sound = Sound_Check(audio_path, sex)

    sound.set_pitch_analysis(sound.extract_pitch(sound.load_wave()))