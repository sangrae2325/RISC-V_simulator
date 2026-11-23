"""main.py - 프로그램 시작점 (담당: A 이상래)

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
    # 주소를 text 메모리 안의 위치(인덱스)로 바꾼다.
    # 예) pc 0x00040014 -> 0x14 (20번째 바이트부터)
    offset = pc - TEXT_START

    # text 영역 밖이면 명령어 값을 0으로 본다.
    # 0은 지원하지 않는 명령어라서 main에서 invalid로 처리되어 정상 종료된다.
    #   offset < 0                  : text 시작 주소보다 앞
    #   offset + 4 > len(text_mem)  : 4바이트를 다 읽을 수 없음 (끝을 넘음)
    if offset < 0 or offset + 4 > len(text_mem):
        return 0

    # little-endian 4바이트 읽기는 memory.read_word가 담당한다.
    return read_word(text_mem, offset)


def main(argv: list) -> int:
    """인수 확인 -> 적재 -> fetch/decode/execute 루프 -> 종료 출력, data.out 저장

    - 인수가 2개가 아니면 표준 오류에 사용법 출력 후 1 반환
    - decode 결과가 None이면: fetch 당시 PC와 명령어 값 출력, data.out 저장, 0 반환
    - 실행 개수가 MAX_STEPS에 도달했는데 다음 명령어가 지원 명령어면: 표준 오류 메시지, 1 반환
    """
    # ---- 1. 인수 확인 ----
    # argv에는 실행 파일 이름을 뺀 인수만 들어온다. (text 경로, data 경로)
    if len(argv) != 2:
        print("usage: python3 main.py text.bin data.bin", file=sys.stderr)
        return 1
    text_path, data_path = argv

    # ---- 2. 적재와 초기화 ----
    text_mem = load_text(text_path)   # bytes, 주소 0x00040000부터
    data_mem = load_data(data_path)   # bytearray(1024), 주소 0x10000000부터
    regs = [0] * 32                   # x0 ~ x31, 모두 0으로 시작
    pc = TEXT_START                   # 초기 PC = 0x00040000
    steps = 0                         # 지금까지 실행한 정상 명령어 개수

    # ---- 3. fetch -> decode -> execute 반복 ----
    while True:
        inst = fetch(text_mem, pc)    # (1) fetch: pc는 여기서 바꾸지 않는다
        d = decode(inst)              # (2) decode: 지원하지 않으면 None

        # (3) invalid: 실행하지 않고 정상 종료
        #     pc는 execute에서만 바뀌므로, 지금 pc가 곧 이 명령어를 fetch한 주소다.
        if d is None:
            print(f"PC 0x{pc:08x} invalid instruction 0x{inst:08x}")
            save_data_out(data_mem)   # 현재 작업 디렉터리에 data.out
            return 0

        # (4) 실행 한도: 이미 1,000,000개를 실행했는데 다음 명령어가 지원 명령어면
        #     실행하지 않고 비정상 종료한다. (invalid 검사를 먼저 하므로
        #     한도 직후 invalid를 만나면 위에서 정상 종료된다)
        if steps >= MAX_STEPS:
            print(f"error: execution limit exceeded ({MAX_STEPS} instructions), "
                  f"next PC 0x{pc:08x}", file=sys.stderr)
            return 1

        # (5) execute: 다음 PC를 돌려받는다. pc가 바뀌는 곳은 여기 한 곳뿐이다.
        pc = execute(d, regs, data_mem, pc)
        steps += 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
