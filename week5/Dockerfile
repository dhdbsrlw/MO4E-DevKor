# Docker 이미지 만들기

FROM amd64/python:3.9-slim

WORKDIR /usr/app 
# 필요시 수정

RUN pip install -U pip \
    && pip install "fastapi[all]"

COPY crud_pydantic.py crud_pydantic.py

# 컨테이너가 실행될 때 수행할 명령어의 기본값 명시
CMD ["uvicorn", "crud_pydantic:app", "--host", "0.0.0.0", "--reload"]