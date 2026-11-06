"""tests/make_test.py - 테스트 만들기 (담당: C 보민)

16진수 명령어를 입력하면 tests/cases/<이름>/ 아래에 다음 파일을 만든다.
    text.bin             명령어(little-endian 바이너리). 마지막은 0x00000000
    data.bin             초기 데이터 (없으면 0바이트 파일)
    expected_stdout.txt  기대 표준 출력 한 줄
    expected_data.out    기대 data.out (1024바이트)
    README.md            테스트 목적 / 어셈블리 / 기대 결과 도출 근거

기대 결과는 시뮬레이터를 돌려서 만들지 말고 손으로 계산해서 적는다.
(같은 버그가 기대값에도 들어가는 것을 막기 위해)
"""

import sys


def words_to_bytes(words: list) -> bytes:
    """32비트 정수 리스트를 little-endian 바이트열로 바꾼다.

    예) [0x100000b7] -> b'\\xb7\\x00\\x00\\x10'
    """
    raise NotImplementedError("TODO(C): words_to_bytes")


def main(argv: list) -> int:
    """사용법(예시, 팀에서 확정):
        python3 tests/make_test.py <이름> <hex1> <hex2> ...
    """
    raise NotImplementedError("TODO(C): main")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
