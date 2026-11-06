"""main.py - 프로그램 시작점 (담당: A 상래)

실행: python3 main.py text.bin data.bin
표준 출력: PC 0x........ invalid instruction 0x........  (한 줄)
파일 출력: 현재 작업 디렉터리의 data.out (1024바이트)
진단 메시지는 표준 오류(sys.stderr)로만 출력한다.
"""

import sys

from utils import TEXT_START, MAX_STEPS
from memory import load_text, load_data, read_word, save_data_out
from decoder import decode
from executor import execute


def fetch(text_mem: bytes, pc: int) -> int:
    """pc - TEXT_START 위치에서 4바이트(little-endian)를 읽는다. 영역 밖이면 0."""
    raise NotImplementedError("TODO(A): fetch")


def main(argv: list) -> int:
    """인수 확인 -> 적재 -> fetch/decode/execute 루프 -> 종료 출력, data.out 저장

    - 인수가 2개가 아니면 표준 오류에 사용법 출력 후 1 반환
    - decode 결과가 None이면: fetch 당시 PC와 명령어 값 출력, data.out 저장, 0 반환
    - 실행 개수가 MAX_STEPS에 도달했는데 다음 명령어가 지원 명령어면: 표준 오류 메시지, 1 반환
    """
    raise NotImplementedError("TODO(A): main")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
