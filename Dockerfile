FROM python:3.7
WORKDIR  /app
COPY . /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
EXPOSE 8000
