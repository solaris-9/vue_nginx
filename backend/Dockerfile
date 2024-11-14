FROM public.ecr.aws/docker/library/python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HTTP_PROXY "http://10.158.100.2:8080/"
ENV HTTPS_PROXY "http://10.158.100.2:8080/"

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update && apt-get install -y python3-dev libldap2-dev libsasl2-dev libssl-dev
RUN mkdir ~/.pip && \  
cd ~/.pip/  && \  
echo "[global] \ntrusted-host =  mirrors.aliyun.com \nindex-url = http://mirrors.aliyun.com/pypi/simple/" >  pip.conf
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt
COPY scripts/start*.sh /
ADD . /code/
EXPOSE 8003
