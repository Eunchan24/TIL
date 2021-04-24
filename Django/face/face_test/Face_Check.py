import cv2
import mediapipe as mp
import numpy as np
from keras.models import load_model
from scipy.spatial import distance
import json
from django.http import JsonResponse, HttpResponse
import os


class Eye_check:
    def __init__(self):
        self.VISIBILITY_THRESHOLD = 0.5
        self.PRESENCE_THRESHOLD = 0.5
        self.Landmark_eye = [
            33, 7, 163, 144, 145, 153, 154, 155,
            133, 246, 161, 160, 159, 158, 157, 173,
            263, 249, 390, 373, 374, 380, 381, 382,
            362, 466, 388, 387, 386, 385, 384, 398
        ]
        self.model = load_model('/home/ubuntu/face/face_test/model/eye_model.h5')
        self.IMG_SIZE = (34, 26)
        self.mp_drawing = mp.solutions.drawing_utils

    # 눈 자르기
    def crop_eye(self, img, eye_points):
        x1, y1 = np.amin(eye_points, axis=0)
        x2, y2 = np.amax(eye_points, axis=0)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        w = (x2 - x1) * 1.2
        h = w * self.IMG_SIZE[1] / self.IMG_SIZE[0]

        margin_x, margin_y = w / 2, h / 2

        min_x, min_y = int(cx - margin_x), int(cy - margin_y)
        max_x, max_y = int(cx + margin_x), int(cy + margin_y)

        eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)
        eye_img = img[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]
        return eye_img, eye_rect

    # 눈 좌표값 np.array 변환
    def to_ndarray(self, dict):
        return np.array([x for i, x in dict.items() if i in self.Landmark_eye])

    # 눈 깜박임 모델 적용, 예측
    def eye_preL(self, eye_img_l, ):
        # 이미지 변경
        eye_img_l = cv2.resize(eye_img_l, dsize=self.IMG_SIZE)

        # 전처리
        eye_input_l = eye_img_l.reshape((1, self.IMG_SIZE[1], self.IMG_SIZE[0], 1)).astype(np.float32) / 255.

        # model 적용 -> 예측
        pred_l = self.model.predict(eye_input_l)

        # 시각화, 0.02보다 높으면(눈 떴을때) 0, 감으면 1 표시
        state_l = '0' if pred_l > 0.02 else '1'

        state_l = state_l % pred_l

        return int(state_l)

    # 눈 깜박임 모델 적용, 예측
    def eye_preR(self, eye_img_r):
        # 이미지 변경
        eye_img_r = cv2.resize(eye_img_r, dsize=self.IMG_SIZE)

        # 전처리
        eye_input_r = eye_img_r.reshape((1, self.IMG_SIZE[1], self.IMG_SIZE[0], 1)).astype(np.float32) / 255.

        # model 적용 -> 예측
        pred_r = self.model.predict(eye_input_r)

        # 시각화, 0.02보다 높으면(눈 떴을때) 0, 감으면 1 표시
        state_r = '0' if pred_r > 0.02 else '1'

        state_r = state_r % pred_r

        return int(state_r)

    # 눈 좌표값 추출 및 마킹
    def eye_drawing(self, landmark_dict, eye_image=None):
        for i in self.Landmark_eye:  # 눈 좌표값만 그리기
            cv2.circle(eye_image, landmark_dict[i], 1, (0, 0, 255), -1)

    # 얼굴 랜드마크 dict 저장
    def landmark_dict(self, results, width, height):
        face_landmark = {}
        for face_landmarks in results.multi_face_landmarks:
            for idx, landmark in enumerate(face_landmarks.landmark):
                if ((landmark.HasField('visibility') and
                     landmark.visibility < self.VISIBILITY_THRESHOLD) or
                        (landmark.HasField('presence') and
                         landmark.presence < self.PRESENCE_THRESHOLD)):
                    continue
                landmark_px = self.mp_drawing._normalized_to_pixel_coordinates(landmark.x, landmark.y, width, height)
                if landmark_px:
                    face_landmark[idx] = landmark_px
        return face_landmark

    # 표정 변화율
    def face_change(self, dict):
        w_line = int(distance.euclidean(dict[227], dict[447]))

        mouth = int(distance.euclidean(dict[61], dict[291]))
        res_mouth = int((mouth / w_line) * 100)

        clown = int(distance.euclidean(dict[50], dict[280]))
        res_clown = int((clown / w_line) * 100)

        brow = int(distance.euclidean(dict[107], dict[336]))
        res_brow = int((brow / w_line) * 100)

        Nasolabial_Folds = int(distance.euclidean(dict[205], dict[425]))
        Nasolabial_Folds_res = int((Nasolabial_Folds / w_line) * 100)

        return res_mouth, res_clown, res_brow, Nasolabial_Folds_res

    # 영상 파일을 삭제해준다.
    def del_file(self, path):
        try:
            os.remove(path)
        except:
            pass

    def face_run(self, viedo_file):
        eye_cnt = 0
        frame = 0
        eye = 0
        eye_list = []
        Nasolabial_Folds_list = []
        brow_list = []
        clown_list = []
        mouth_list = []

        cap = cv2.VideoCapture(viedo_file)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        m_fps = cap.get(cv2.CAP_PROP_FPS) * 60  # 분당 프레임
        face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        check = Eye_check()

        # 캠 실행
        while cap.isOpened():
            ret, image = cap.read()

            if not ret:
                print("End frame")
                eye_list.append(int(eye_cnt / 2))
                break

            frame += 1
            if frame % m_fps == 0:
                eye_list.append(int(eye_cnt / 2))
                eye_cnt = 0
                frame = 0

            # 얼굴 좌표값 받기
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)

            # 얼굴 좌표 그리기 준비
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 눈 인식 표시만 할 이미지 복사
            eye_image = image.copy()

            if results.multi_face_landmarks:
                # 얼굴 랜드마크 dict 저장
                idx_to_coordinates = check.landmark_dict(results, width, height)

                # 눈 좌표 np.array 변환
                eye_np = check.to_ndarray(idx_to_coordinates)

                # 눈 부분 crop, 주의! 오른쪽부터 나올 경우 안됨, 입장시 왼쪽으로 입장해주세요
                eye_img_l, eye_rect_l = check.crop_eye(gray, eye_points=eye_np[0:16])  # 왼쪽 눈
                eye_img_r, eye_rect_r = check.crop_eye(gray, eye_points=eye_np[16:32])  # 오른쪽 눈

                state_r = check.eye_preR(eye_img_r)
                state_l = check.eye_preL(eye_img_l)

                state = 1 if state_l == 1 or state_r == 1 > 0.05 else 0

                # 눈 깜빡임 카운트
                if eye != state:
                    eye = state
                    eye_cnt += 1
                else:
                    eye = state

                # 표정 변화율
                res_mouth, res_clown, res_brow, Nasolabial_Folds_res = check.face_change(idx_to_coordinates)

                mouth_list.append(res_mouth)
                clown_list.append(res_clown)
                brow_list.append(res_brow)
                Nasolabial_Folds_list.append(Nasolabial_Folds_res)

            # cv2.imshow('MediaPipe EyeMesh', eye_image)  # 눈 인식 표시
            if cv2.waitKey(1) == ord('q'):
                eye_list.append(int(eye_cnt / 2))
                break

        face_mesh.close()
        cap.release()
        cv2.destroyAllWindows()

        face_json = {

            'eye': {
                'x': len(eye_list),
                'y': eye_list
            },
            'face': {
                'mouth': {
                    'x': len(mouth_list),
                    'y': mouth_list
                },
                'clown': {
                    'x': len(clown_list),
                    'y': clown_list
                },
                'brow': {
                    'x': len(brow_list),
                    'y': brow_list
                },
                'nasolabial_folds': {
                    'x': len(Nasolabial_Folds_list),
                    'y': Nasolabial_Folds_list
                }

            }

        }
        check.del_file(viedo_file)

        return face_json