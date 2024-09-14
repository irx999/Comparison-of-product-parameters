FROM python:3.12-alpine
WORKDIR /src

COPY main.py /src
COPY requirements.txt /src

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


CMD ["streamlit","run","main.py"]
