FROM docker.m.daocloud.io/python:3.12.8

WORKDIR /app
COPY . /app 

RUN pip install --progress-bar off -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 60
RUN pip install --progress-bar off -U setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 60
RUN pip install --progress-bar off --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--lifespan", "on"]
