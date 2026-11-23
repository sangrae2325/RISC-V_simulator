"""tests/run_tests.py - 전체 테스트 실행 (담당: A 이상래)

실행: python3 tests/run_tests.py            (전체)
      python3 tests/run_tests.py t01 t07    (이름에 t01 또는 t07이 들어간 케이스만)

tests/cases/ 아래 폴더마다:
  1. 임시 폴더를 작업 디렉터리로 해서 main.py text.bin data.bin 실행
     (data.out이 현재 작업 디렉터리에 생기므로)
  2. 표준 출력 == expected_stdout.txt 인지 비교
  3. 생성된 data.out == expected_data.out 인지 바이트 단위 비교
  4. PASS / FAIL 출력, 하나라도 FAIL이면 종료 코드 1
"""

import os
import subprocess
import sys
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TESTS_DIR)            # main.py가 있는 폴더
CASES_DIR = os.path.join(TESTS_DIR, "cases")
MAIN_PY = os.path.join(ROOT_DIR, "main.py")
TIMEOUT_SEC = 60                                 # 한 케이스 최대 실행 시간


def read_file(path: str, binary: bool):
    """파일을 읽는다. 없으면 None."""
    if not os.path.exists(path):
        return None
    with open(path, "rb" if binary else "r", **({} if binary else {"encoding": "utf-8"})) as f:
        return f.read()


def first_diff(a: bytes, b: bytes) -> str:
    """두 바이트열이 처음 달라지는 위치를 설명한다. (실패 원인 찾기용)"""
    if len(a) != len(b):
        return f"크기 다름: 실제 {len(a)}바이트, 기대 {len(b)}바이트"
    for i in range(len(a)):
        if a[i] != b[i]:
            start = i - i % 4                    # 4바이트 단위로 보여 준다
            return (f"오프셋 {i} (주소 0x{0x10000000 + i:08x})부터 다름: "
                    f"실제 {a[start:start + 4].hex(' ')}, 기대 {b[start:start + 4].hex(' ')}")
    return "같음"


def run_one(case_dir: str) -> bool:
    """테스트 하나를 실행하고 통과 여부를 반환한다."""
    name = os.path.basename(case_dir)
    text_bin = os.path.join(case_dir, "text.bin")
    data_bin = os.path.join(case_dir, "data.bin")
    expected_stdout = read_file(os.path.join(case_dir, "expected_stdout.txt"), binary=False)
    expected_data = read_file(os.path.join(case_dir, "expected_data.out"), binary=True)

    if expected_stdout is None or expected_data is None or not os.path.exists(text_bin):
        print(f"FAIL  {name}: text.bin / expected_stdout.txt / expected_data.out 중 빠진 파일이 있음")
        return False

    # data.bin이 없는 케이스도 있을 수 있으므로, 없으면 빈 파일을 대신 쓴다.
    with tempfile.TemporaryDirectory() as work:
        if not os.path.exists(data_bin):
            data_bin = os.path.join(work, "empty_data.bin")
            open(data_bin, "wb").close()

        # 임시 폴더(work)를 작업 디렉터리로 실행 -> data.out이 여기에 생긴다.
        try:
            result = subprocess.run(
                [sys.executable, MAIN_PY, text_bin, data_bin],
                cwd=work, capture_output=True, text=True, timeout=TIMEOUT_SEC,
            )
        except subprocess.TimeoutExpired:
            print(f"FAIL  {name}: {TIMEOUT_SEC}초 안에 끝나지 않음")
            return False

        actual_data = read_file(os.path.join(work, "data.out"), binary=True)

    problems = []
    if result.returncode != 0:
        problems.append(f"종료 코드 {result.returncode} (stderr: {result.stderr.strip()[-200:]})")
    if result.stdout != expected_stdout:
        problems.append(f"표준 출력 다름: 실제 {result.stdout!r}, 기대 {expected_stdout!r}")
    if actual_data is None:
        problems.append("data.out이 생성되지 않음")
    elif actual_data != expected_data:
        problems.append("data.out " + first_diff(actual_data, expected_data))

    if problems:
        print(f"FAIL  {name}")
        for p in problems:
            print(f"      - {p}")
        return False
    print(f"PASS  {name}")
    return True


def main() -> int:
    filters = sys.argv[1:]
    if not os.path.isdir(CASES_DIR):
        print(f"테스트 폴더가 없음: {CASES_DIR}", file=sys.stderr)
        return 1

    cases = sorted(
        d for d in os.listdir(CASES_DIR)
        if os.path.isdir(os.path.join(CASES_DIR, d))
        and (not filters or any(f in d for f in filters))
    )
    if not cases:
        print("실행할 테스트가 없음", file=sys.stderr)
        return 1

    passed = sum(run_one(os.path.join(CASES_DIR, c)) for c in cases)
    print(f"\n{passed}/{len(cases)} passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
