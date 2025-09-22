FROM python:3.12.5-slim
LABEL authors="d1z"

WORKDIR /quiz_prep

RUN python -m venv /quiz_prep/venv
ENV PATH="/quiz_prep/venv/bin:$PATH"

COPY requirements.txt /quiz_prep
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src

CMD ["python", "-m", "src.main"]