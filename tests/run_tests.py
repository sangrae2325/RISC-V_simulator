"""tests/run_tests.py - 전체 테스트 실행 (담당: A 상래)

실행: python3 tests/run_tests.py

tests/cases/ 아래 폴더마다:
  1. 임시 폴더를 작업 디렉터리로 해서 main.py text.bin data.bin 실행
     (data.out이 현재 작업 디렉터리에 생기므로)
  2. 표준 출력 == expected_stdout.txt 인지 비교
  3. 생성된 data.out == expected_data.out 인지 바이트 단위 비교
  4. PASS / FAIL 출력, 하나라도 FAIL이면 종료 코드 1
"""

import sys


def run_one(case_dir: str) -> bool:
    """테스트 하나를 실행하고 통과 여부를 반환한다."""
    raise NotImplementedError("TODO(A): run_one")


def main() -> int:
    raise NotImplementedError("TODO(A): main")


if __name__ == "__main__":
    sys.exit(main())
