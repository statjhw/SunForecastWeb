FROM python:3.9.7-bullseye

WORKDIR /streamlit/

COPY ./streamlit .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "practice.py", "--server.port=8501", "--server.address=0.0.0.0"]

