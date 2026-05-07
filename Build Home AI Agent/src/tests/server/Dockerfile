FROM python:3.12-slim
RUN useradd -m appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt
COPY app.py .
USER appuser
EXPOSE 10031

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:10031/health')" || exit 1

CMD ["gunicorn", \
     "--bind", "0.0.0.0:10031", \
     "--workers", "4", \
     "--worker-class", "gevent", \
     "--worker-connections", "1000", \
     "--timeout", "600", \
     "--keep-alive", "75", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--graceful-timeout", "300", \
     "app:app"]