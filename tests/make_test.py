"""tests/make_test.py - 테스트 만들기 (담당: C 보민)

16진수 명령어를 입력하면 tests/cases/<이름>/ 아래에 다음 파일을 만든다.
    text.bin             명령어(little-endian 바이너리). 마지막은 0x00000000
    data.bin             초기 데이터 (없으면 0바이트 파일)
    expected_stdout.txt  기대 표준 출력 한 줄
    expected_data.out    기대 data.out (1024바이트)
    README.md            테스트 목적 / 어셈블리 / 기대 결과 도출 근거

기대 결과는 시뮬레이터를 돌려서 만들지 말고 손으로 계산해서 적는다.
(같은 버그가 기대값에도 들어가는 것을 막기 위해)

사용 예 (명세서 7절 예시):
    python3 tests/make_test.py t01 \\
        0x100000b7 0x00700113 0x00500193 0x00310233 0x0040a023 \\
        --asm "lui x1, 0x10000" "addi x2, x0, 7" "addi x3, x0, 5" \\
              "add x4, x2, x3" "sw x4, 0(x1)" \\
        --purpose "명세서 7절 기능 확인 예시" \\
        --expect-data 0:0c000000
"""

import argparse
import os
import sys

# tests/ 폴더에서 실행해도 상위 폴더의 utils.py를 import 할 수 있게 한다.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import DATA_SIZE, TEXT_START  # noqa: E402

DEFAULT_OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases")


def words_to_bytes(words: list) -> bytes:
    """32비트 정수 리스트를 little-endian 바이트열로 바꾼다.

    예) [0x100000b7] -> b'\\xb7\\x00\\x00\\x10'
    """
    out = bytearray()
    for w in words:
        if not 0 <= w <= 0xFFFFFFFF:
            raise ValueError(f"32비트 범위를 벗어난 값: {w:#x}")
        out += w.to_bytes(4, "little")
    return bytes(out)


def parse_word(text: str) -> int:
    """'0x100000b7', '100000b7', '0x1000_00b7' 형태의 16진수를 32비트 정수로 바꾼다."""
    s = text.strip().replace("_", "")
    if s[:2].lower() == "0x":
        s = s[2:]
    if not s or len(s) > 8:
        raise ValueError(f"32비트 16진수가 아님: {text!r}")
    return int(s, 16)


def parse_hex_bytes(text: str) -> bytes:
    """'0c000000' 또는 '0c 00 00 00' 형태의 16진수 바이트열을 바이트로 바꾼다."""
    s = text.replace(" ", "").replace("_", "")
    if s[:2].lower() == "0x":
        s = s[2:]
    if len(s) % 2:
        raise ValueError(f"16진수 자릿수가 홀수: {text!r}")
    return bytes.fromhex(s)


def build_expected_data(data: bytes, patches: list) -> bytes:
    """기대 data.out을 만든다.

    data.bin 내용을 1,024바이트로 0 채움한 값에서 시작해, 손으로 계산한
    (오프셋, 바이트열) 패치를 덮어쓴다. (시뮬레이터를 돌리지 않는다.)
    """
    buf = bytearray(DATA_SIZE)
    buf[: len(data)] = data
    for offset, chunk in patches:
        if offset < 0 or offset + len(chunk) > DATA_SIZE:
            raise ValueError(f"data 영역(0~{DATA_SIZE - 1}) 밖: 오프셋 {offset}, {len(chunk)}바이트")
        buf[offset : offset + len(chunk)] = chunk
    return bytes(buf)


def parse_patch(text: str):
    """'<오프셋>:<hex바이트>' -> (오프셋, bytes). 오프셋은 10진수 또는 0x 16진수."""
    if ":" not in text:
        raise ValueError(f"'오프셋:hex' 형식이 아님: {text!r}")
    off, chunk = text.split(":", 1)
    return int(off, 0), parse_hex_bytes(chunk)


def default_stdout(words: list) -> str:
    """직선 실행(분기 없음)을 가정한 기대 표준 출력.

    마지막 단어(0x00000000)를 fetch 했을 때 종료하므로 PC는 그 단어의 주소다.
    분기로 흐름이 바뀌는 테스트는 --expect-stdout 으로 직접 지정한다.
    """
    pc = TEXT_START + 4 * (len(words) - 1)
    return f"PC 0x{pc:08x} invalid instruction 0x{words[-1]:08x}"


def make_readme(name, purpose, asm, words, data, stdout_line, patches, stdout_is_default) -> str:
    lines = [f"# {name}", "", "## 목적", purpose or "(미기재)", ""]
    lines += ["## 명령어", "", "| 주소 | 기계어 | 어셈블리 |", "| --- | --- | --- |"]
    for i, w in enumerate(words):
        a = asm[i] if i < len(asm) else ("invalid instruction (종료)" if i == len(words) - 1 else "")
        lines.append(f"| 0x{TEXT_START + 4 * i:08x} | 0x{w:08x} | {a} |")
    lines += ["", "## 초기 data.bin", f"{len(data)}바이트" + (f": `{data.hex()}`" if data else ""), ""]
    lines += ["## 기대 결과 도출 근거", ""]
    lines.append(f"- 표준 출력: `{stdout_line}`")
    if stdout_is_default:
        lines.append("  - 분기 없는 직선 실행을 가정해, 마지막 단어의 주소와 값으로 계산했다.")
    if patches:
        for off, chunk in patches:
            lines.append(f"- data.out 오프셋 {off}: `{chunk.hex()}` (그 밖의 바이트는 data.bin 내용, 없으면 0)")
    else:
        lines.append("- data.out: data.bin 내용을 0으로 채워 1,024바이트로 맞춘 값 (메모리 쓰기 없음)")
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="RISC-V 시뮬레이터 테스트 케이스 생성")
    p.add_argument("name", help="테스트 이름 (tests/cases/<이름>/ 에 생성)")
    p.add_argument("words", nargs="+", help="16진수 명령어 (예: 0x100000b7)")
    p.add_argument("--data", default="", help="data.bin 내용 (16진수 바이트열, 최대 1024바이트)")
    p.add_argument("--asm", nargs="*", default=[], help="명령어별 어셈블리 설명 (README용)")
    p.add_argument("--purpose", default="", help="테스트 목적 (README용)")
    p.add_argument("--expect-stdout", default=None, help="기대 표준 출력 한 줄 (생략 시 직선 실행 가정)")
    p.add_argument("--expect-data", nargs="*", default=[], metavar="OFF:HEX",
                   help="기대 data.out 에서 바뀌는 부분. 예: 0:0c000000")
    p.add_argument("--out-dir", default=DEFAULT_OUT_DIR, help="케이스를 만들 폴더 (기본: tests/cases)")
    p.add_argument("--force", action="store_true", help="같은 이름의 케이스를 덮어쓴다")
    return p


def main(argv: list) -> int:
    """사용법:
        python3 tests/make_test.py <이름> <hex1> <hex2> ... [옵션]
    옵션은 --help 참고.
    """
    args = build_parser().parse_args(argv)

    if not args.name or os.path.basename(args.name) != args.name or args.name in (".", ".."):
        print(f"잘못된 테스트 이름: {args.name!r}", file=sys.stderr)
        return 1

    try:
        words = [parse_word(w) for w in args.words]
        data = parse_hex_bytes(args.data)
        if len(data) > DATA_SIZE:
            raise ValueError(f"data.bin 은 최대 {DATA_SIZE}바이트 (입력 {len(data)}바이트)")
        patches = [parse_patch(t) for t in args.expect_data]
        # text.bin 의 마지막 4바이트는 0x00000000 (종료용 invalid instruction)
        if words[-1] != 0:
            words.append(0)
        expected_data = build_expected_data(data, patches)
    except ValueError as e:
        print(f"입력 오류: {e}", file=sys.stderr)
        return 1

    stdout_is_default = args.expect_stdout is None
    stdout_line = default_stdout(words) if stdout_is_default else args.expect_stdout

    case_dir = os.path.join(args.out_dir, args.name)
    if os.path.exists(case_dir) and not args.force:
        print(f"이미 있음: {case_dir} (덮어쓰려면 --force)", file=sys.stderr)
        return 1
    os.makedirs(case_dir, exist_ok=True)

    def write(fname: str, content, binary: bool) -> None:
        with open(os.path.join(case_dir, fname), "wb" if binary else "w",
                  **({} if binary else {"encoding": "utf-8", "newline": "\n"})) as f:
            f.write(content)

    write("text.bin", words_to_bytes(words), True)
    write("data.bin", data, True)
    write("expected_stdout.txt", stdout_line + "\n", False)
    write("expected_data.out", expected_data, True)
    write("README.md", make_readme(args.name, args.purpose, args.asm, words, data,
                                   stdout_line, patches, stdout_is_default), False)
    print(f"생성: {case_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
