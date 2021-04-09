from __future__ import print_function
import time
import boto3
import re

pattern = re.compile(r'.+')

# 음성 파일 경로를 넣어주세요 by.기훈
file_name = '/Users/eunchankim/Downloads/man/man_2.wav'
# 음성 파일을 저장할 아마존 S3 버켓입니다. by.기훈
bucket_name = 'goofanaka-stt-test'
# 파일 이름 변경 by.은찬
file_real_name = file_name.split('/')[-1]
print(file_real_name)
# boto3는 아마존 aws 서비스를 파이썬에서 사용하기 위한 라이브러리 입니다.
# 없다면 꼭 설치를 바랍니다. by.기훈
s3 = boto3.client('s3', # 사용할 서비스 이름 by.기훈
                  aws_access_key_id='', # 액세스키 by.기훈
                  aws_secret_access_key='', # 시크릿 키 by.기훈
                  region_name='' # 사용하는 서버 위치 by.기훈
                  )

# s3 버켓에 업로드하는 코드 입니다. by.기훈
s3.upload_file(file_name , # 버켓에 저장할 파일의 경로 입니다.
               bucket_name, # 저장 할 버켓의 이름입니다.
               'man_2.wav') # 버켓에 저장될 파일 이름입니다.

## 여기서 부터는 aws transcribe에 넣기 위한 코드입니다.

# s3 버켓의 경로입니다.
s3_uri = f's3://{bucket_name}/'
print(s3_uri)
file_format = file_name[file_name.find('.')+1:]
print(file_format)
transcribe = boto3.client('transcribe',
                          aws_access_key_id='',
                          aws_secret_access_key='',
                          region_name=''
                          )
job_name = "file_real_name"
job_uri = f"s3://{bucket_name}/{file_real_name}"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name, # 중복 노노, 이름은 자유롭게 설정 가능
    Media={'MediaFileUri': job_uri}, # s3 버켓에 올라가 있는 음성 파일 경로(s3-uri)
    MediaFormat=file_format, # 파일의 포맷(m4a = mp4, mp3, wav, flac...)
    LanguageCode='ko-KR' # 언어 설정
)

while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
print(status)