# (과제) REST API 설계 및 FastAPI 구현

목표: DevKor 회원 관리 시스템을 구축한다. \
조건: DevKor 회원은 id(int), name(string), age(int), role(string) 총 4가지의 property 를 가지고 있다.

## 구현하여야 하는 기능

1. 전체 사용자 조회
2. 사용자의 id 를 이용하여 특정 사용자 조회
3. 특정 id 를 가진 사용자 정보 업데이트
4. 특정 id 를 가진 사용자의 회원 탈퇴
5. 사용자 정보 생성 (추가)

### API 명세서

1. 전체 사용자 조회

- HTTP: GET
- URI: /users

2. 특정 사용자 조회

- HTTP: GET
- URI: /user

3. 특정 사용자 정보 수정 (업데이트)

- HTTP: PUT
- URI: /user

4. 특정 사용자 회원 탈퇴

- HTTP: DELETE
- URI: /user

5. 사용자 정보 생성 (추가)

- HTTP: POST
- URI: /user