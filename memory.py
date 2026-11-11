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
    # "rb" = 바이너리 읽기 모드. 글자가 아니라 바이트 그대로 읽는다.
    # with를 쓰면 블록이 끝날 때 파일이 자동으로 닫힌다.
    with open(path, "rb") as f:
        text = f.read()   # 파일 전체를 bytes로 읽음 (헤더 없음, 0번 바이트 = 주소 TEXT_START)

    # text 메모리는 읽기만 하므로 바꿀 수 없는 bytes 그대로 반환한다.
    return text


def load_data(path: str) -> bytearray:
    """DATA_SIZE 바이트를 0으로 만든 뒤 data.bin 내용을 앞에서부터 복사해 반환한다.

    data.bin 크기는 0~1024 바이트.
    """
    # 1. 크기 1024짜리 바이트 배열을 만든다. 처음엔 전부 0이다.
    #    bytearray는 bytes와 달리 내용을 바꿀 수 있어서 sw로 쓸 수 있다.
    data = bytearray(DATA_SIZE)

    # 2. data.bin을 바이너리로 읽는다. (크기 0 ~ 1024 바이트)
    with open(path, "rb") as f:
        content = f.read()

    # 3. 읽은 내용을 앞(인덱스 0 = 주소 DATA_START)에서부터 한 바이트씩 복사한다.
    #    data.bin이 1024보다 작으면 나머지는 0으로 남는다.
    #    크기가 0이면 반복이 한 번도 안 돌고, 전부 0인 메모리가 된다.
    #    min(...)은 혹시 1024보다 큰 파일이 와도 배열 밖으로 넘치지 않게 하는 안전장치.
    for i in range(min(len(content), DATA_SIZE)):
        data[i] = content[i]

    return data


def read_word(mem, offset: int) -> int:
    """mem[offset]부터 4바이트를 little-endian으로 읽는다.

    값 = b0 + (b1<<8) + (b2<<16) + (b3<<24)
    예) 바이트 78 56 34 12 -> 0x12345678
    """
    # little-endian: 가장 낮은 주소에 가장 낮은(작은) 바이트가 들어 있다.
    b0 = mem[offset]       # 비트  0 ~  7 (가장 낮은 바이트)
    b1 = mem[offset + 1]   # 비트  8 ~ 15
    b2 = mem[offset + 2]   # 비트 16 ~ 23
    b3 = mem[offset + 3]   # 비트 24 ~ 31 (가장 높은 바이트)

    # 각 바이트를 제자리(8비트씩)로 밀어서 더한다.
    # 예) 78 56 34 12 -> 0x78 + 0x5600 + 0x340000 + 0x12000000 = 0x12345678
    # 바이트 하나는 0~255라서 서로 겹치지 않으므로 + 로 합쳐도 된다.
    return b0 + (b1 << 8) + (b2 << 16) + (b3 << 24)


def write_word(mem: bytearray, offset: int, value: int) -> None:
    """value(32비트)를 mem[offset]부터 little-endian으로 저장한다.

    가장 낮은 바이트를 가장 낮은 주소(offset)에 저장.
    """
    # read_word의 반대. 오른쪽으로 밀어서 원하는 바이트를 맨 아래로 내린 뒤
    # & 0xFF 로 그 8비트만 남긴다.
    # 예) value = 0x12345678
    #     mem[offset]     = 0x78  (가장 낮은 바이트 -> 가장 낮은 주소)
    #     mem[offset + 1] = 0x56
    #     mem[offset + 2] = 0x34
    #     mem[offset + 3] = 0x12
    mem[offset]     = value & 0xFF
    mem[offset + 1] = (value >> 8) & 0xFF
    mem[offset + 2] = (value >> 16) & 0xFF
    mem[offset + 3] = (value >> 24) & 0xFF


def save_data_out(data_mem: bytearray, path: str = "data.out") -> None:
    """data_mem 1024바이트를 바이너리로 그대로 저장한다. (기존 파일 덮어쓰기)"""
    # "wb" = 바이너리 쓰기 모드. 파일이 있으면 내용을 지우고 새로 쓴다(덮어쓰기).
    # path를 따로 안 주면 현재 폴더에 data.out으로 저장된다.
    with open(path, "wb") as f:
        f.write(data_mem)   # 1024바이트 그대로 저장 (줄바꿈 등 아무것도 추가 안 함)


if __name__ == "__main__":
    # python memory.py 로 단독 확인
    m = bytearray(DATA_SIZE)
    write_word(m, 0, 0x12345678)
    assert bytes(m[0:4]) == bytes([0x78, 0x56, 0x34, 0x12])
    assert read_word(m, 0) == 0x12345678
    print("memory OK")
