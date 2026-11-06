# RISC-V 시뮬레이터

RV32I 중 14개 명령어(add, sub, and, or, addi, andi, ori, lui, lw, sw, beq, bne, blt, bge)를 실행하는 기능 시뮬레이터.

## 팀원

| 역할 | 이름 | 담당 파일 |
| --- | --- | --- |
| A | 이상래 | `main.py`, `tests/run_tests.py`, `README.md` |
| B | 류진 | `utils.py`, `memory.py`, `executor.py`의 `exec_load`, `exec_store` |
| C | 김보민 | `decoder.py`, `tests/make_test.py` |
| D | 김해인 | `executor.py`의 `set_reg`, `exec_r`, `exec_i`, `exec_lui`, `exec_branch` |

## 언어·버전·의존성

- Python 3.10 이상 (TODO: 최종 확인한 버전 기재)
- 외부 라이브러리 없음 (표준 라이브러리만 사용)

## 실행 방법

```bash
python3 main.py text.bin data.bin
```

- 표준 출력: `PC 0x00040014 invalid instruction 0x00000000` 형식의 한 줄
- 현재 작업 디렉터리에 `data.out`(1,024바이트) 생성

## 테스트

```bash
python3 tests/make_test.py <이름> <hex명령어...>   # 테스트 생성
python3 tests/run_tests.py                        # 전체 테스트 실행
```

## 파일 배치

```
riscv-simulator/
├── main.py          # 시작점, fetch, 실행 루프, 종료 출력
├── utils.py         # 상수, to_u32, to_signed, sign_extend
├── memory.py        # text/data 적재, read_word/write_word, data.out 저장
├── decoder.py       # 필드 분해, 즉시값, decode (invalid -> None)
├── executor.py      # execute, set_reg, exec_* 명령어 실행
└── tests/
    ├── make_test.py
    ├── run_tests.py
    └── cases/
        └── t01/     # text.bin, data.bin, expected_stdout.txt, expected_data.out, README.md
```

## 작업 규칙

- import 방향: `main → memory/decoder/executor → utils` (utils는 아무것도 import 하지 않음)
- 함수 이름·인자·반환 형식은 뼈대 그대로 유지. 바꿔야 하면 팀 채팅에 먼저 공유
- 각자 브랜치에서 작업 후 PR로 `main`에 합치기 (예: `feat/utils`, `feat/decoder`)
- 표준 출력에는 종료 줄 외에 아무것도 출력하지 않기 (디버깅은 `sys.stderr`)
- 각 파일은 `python3 파일이름.py`로 단독 실행해서 확인 가능
