FROM fushisanlang/chrome
WORKDIR /spriders

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
EXPOSE 5000
CMD ["python", "MainApp.py"]