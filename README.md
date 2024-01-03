# pykiwoom_rest
키움증권 Open API의 기능을 FastAPI Python Web Framework를 이용해서 REST 서비스로 만듬

## 프로그램 설치 방법

- Release mode 실행
```
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 10 --log-config env/log_conf.ini

```
- Debug mode 실행
```
uvicorn main:app --host 0.0.0.0 --port 8000 --log-config env/log_conf.ini --reload
```

## 키움 OpenAPI 설치 방법

`https://wikidocs.net/8942` 참고  
최신 FastAPI 사용 기법을 위해서 python 3.10 이상을 설치하며 Kiwoom Open API 사용을 위해 Win32 python을 설치한다.

### Anaconda에서 python 3.10 32bit 가상 환경 생성

- 가상환경 생성
```
conda create -n py310_32
conda activate py310_32
conda config --env --set subdir win-32
conda install python=3.10
```

- 32bit 확인
```
conda info
.... <명령 출력 결과 확인>
               platform : win-32

```
