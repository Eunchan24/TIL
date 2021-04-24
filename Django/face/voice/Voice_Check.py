import parselmouth
import numpy as np
import plotly.graph_objects as go
import os

# 음성 분석 클래스 입니다. by.동건,은찬
class Sound_Check_Class:

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
        self.sound_model(interpolated, pitch_analysis)


    # pitch 분석 모델 입니다. by.동건,은찬
    def sound_model(self, interpolated, pitch_analysis):
        mean = int(round(np.nanmean(interpolated)))
        std = int(round(np.nanstd(interpolated)))
        print(mean)
        print(std)
        print(interpolated)
        print(pitch_analysis.xs())
        # 평균(mean)과, 표준편차(std) 분석하는 코드입니다. by.동건,은찬
        if self.sex == 'man':
            if std < 20:
                return mean, print("너무 단조롭다")

            elif std >= 20 and std < 30:
                return mean, print("무난하다")

            elif std >= 30 and std <= 55:
                return mean, print("아나운서와 유사, good")

            elif std > 55:
                return mean, print("너무 산만하거나, 너무 긴장한다.")

        elif self.sex == 'woman':
            if std < 45:
                return mean, print("너무 단조롭다")

            elif std >= 45 and std < 55:
                return mean, print("무난하다")

            elif std >= 55 and std <= 70:
                return mean, print("아나운서와 유사, good")

            elif std > 70:
                return mean, print("너무 산만하거나, 너무 긴장한다.")

    # 파일삭제 함수
    def del_file(self, path):
        try:
            os.remove(path)
        except:
            pass

# 메인 실행 함수 입니다. by.동건,은찬
    def voice_run(self, audio_path, pitch_analysis, interpolated):
        # wav 파일 위치 by.동건,은찬
        audio_path = '/Users/eunchankim/Desktop/IT/ssca_en-core/Goofenaka/Goofenaka_Second_project/sound/voice_project/woman/woman_02.wav'
        # 성별 선택('man', 'woman') by.동건,은찬
        sex = 'woman'
        sound = Sound_Check(audio_path, sex)

        sound.set_pitch_analysis(sound.extract_pitch(sound.load_wave()))

        voice_json = {
            "voice": {
                "x": pitch_analysis.xs(),
                "y": interpolated
            },
            "voice_mean" : int(round(np.nanmean(interpolated))),
            "voice_std" : int(round(np.nanstd(interpolated)))

        }
        Sound_Check.del_file()

        return voice_json