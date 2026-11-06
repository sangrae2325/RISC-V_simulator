"""memory.py - 메모리와 파일 담당 (담당: B 진)

- text_mem: bytes      (text.bin 내용 그대로, 주소 TEXT_START부터)
- data_mem: bytearray  (정확히 DATA_SIZE 바이트, 주소 DATA_START부터)

read_word / write_word 는 '주소'가 아니라 바이트 배열 안의 '오프셋(index)'을 받는다.
  - fetch:      offset = pc - TEXT_START
  - lw / sw:    offset = addr - DATA_START
"""

from utils import DATA_SIZE


def load_text(path: str) -> bytes:
    """text.bin을 바이너리로 읽어 bytes 그대로 반환한다."""
    raise NotImplementedError("TODO(B): load_text")


def load_data(path: str) -> bytearray:
    """DATA_SIZE 바이트를 0으로 만든 뒤 data.bin 내용을 앞에서부터 복사해 반환한다.

    data.bin 크기는 0~1024 바이트.
    """
    raise NotImplementedError("TODO(B): load_data")


def read_word(mem, offset: int) -> int:
    """mem[offset]부터 4바이트를 little-endian으로 읽는다.

    값 = b0 + (b1<<8) + (b2<<16) + (b3<<24)
    예) 바이트 78 56 34 12 -> 0x12345678
    """
    raise NotImplementedError("TODO(B): read_word")


def write_word(mem: bytearray, offset: int, value: int) -> None:
    """value(32비트)를 mem[offset]부터 little-endian으로 저장한다.

    가장 낮은 바이트를 가장 낮은 주소(offset)에 저장.
    """
    raise NotImplementedError("TODO(B): write_word")


def save_data_out(data_mem: bytearray, path: str = "data.out") -> None:
    """data_mem 1024바이트를 바이너리로 그대로 저장한다. (기존 파일 덮어쓰기)"""
    raise NotImplementedError("TODO(B): save_data_out")


if __name__ == "__main__":
    # python memory.py 로 단독 확인
    m = bytearray(DATA_SIZE)
    write_word(m, 0, 0x12345678)
    assert bytes(m[0:4]) == bytes([0x78, 0x56, 0x34, 0x12])
    assert read_word(m, 0) == 0x12345678
    print("memory OK")
