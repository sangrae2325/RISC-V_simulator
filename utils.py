"""utils.py - 여러 파일이 같이 쓰는 도구와 상수 (담당: B 진)

이 파일은 아무것도 import 하지 않는다. (순환 import 방지)
"""

# ---- 공통 상수 ----
TEXT_START = 0x00040000   # text segment 시작 주소 = 초기 PC
DATA_START = 0x10000000   # data segment 시작 주소
DATA_SIZE = 1024          # 데이터 메모리 크기(바이트)
MAX_STEPS = 1_000_000     # 정상 명령어 최대 실행 개수


def to_u32(x: int) -> int:
    """하위 32비트만 남긴다. (x & 0xFFFFFFFF)

    예) to_u32(-1) == 0xFFFFFFFF, to_u32(0x1_0000_0005) == 5
    """
    # 파이썬 정수는 크기 제한이 없어서 덧셈 결과가 32비트를 넘거나 음수가 될 수 있다.
    # 0xFFFFFFFF(1이 32개)와 AND 하면 하위 32비트만 남는다.
    # 음수도 2의 보수 형태로 바뀐다:  -1 & 0xFFFFFFFF == 0xFFFFFFFF
    return x & 0xFFFFFFFF


def to_signed(x: int) -> int:
    """32비트 값을 부호 있는 정수로 해석한다. (blt, bge에서 사용)

    예) to_signed(0xFFFFFFFF) == -1, to_signed(1) == 1
    """
    # 혹시 32비트보다 큰 값이 들어와도 하위 32비트만 보고 판단한다.
    x = x & 0xFFFFFFFF

    # 0x80000000 = 31번 비트(가장 왼쪽 비트)만 1인 값. 이 비트가 부호 비트다.
    if x & 0x80000000:
        # 부호 비트가 1이면 음수.
        # 2의 보수에서 32비트 값 x가 뜻하는 음수는 x - 2^32 이다.
        # 예) 0xFFFFFFFF(4294967295) - 0x100000000(4294967296) = -1
        return x - 0x100000000

    # 부호 비트가 0이면 양수라서 그대로 반환한다.
    return x


def sign_extend(value: int, bits: int) -> int:
    """bits 비트짜리 value를 부호 확장한다. 최상위 비트가 1이면 음수로.

    반환값은 파이썬 int(음수 가능). 레지스터에 넣을 때는 set_reg가 to_u32 한다.
    예) sign_extend(0xFFF, 12) == -1, sign_extend(0x7FF, 12) == 2047
    """
    # (1 << bits) - 1 = 1이 bits개 있는 값. 예) bits=12 이면 0xFFF
    # bits보다 위쪽에 남은 비트가 있으면 지워서 bits 길이만 남긴다.
    value = value & ((1 << bits) - 1)

    # 1 << (bits - 1) = 최상위 비트(부호 비트)만 1인 값. 예) bits=12 이면 0x800
    if value & (1 << (bits - 1)):
        # 부호 비트가 1이면 음수. to_signed와 같은 원리로 2^bits를 뺀다.
        # 예) 0xFFF(4095) - 0x1000(4096) = -1
        #     0x800(2048) - 0x1000(4096) = -2048 (12비트로 표현 가능한 가장 작은 수)
        return value - (1 << bits)

    # 부호 비트가 0이면 양수라서 그대로 반환한다. 예) 0x7FF -> 2047
    return value


if __name__ == "__main__":
    # python utils.py 로 단독 확인
    assert to_u32(-1) == 0xFFFFFFFF
    assert to_signed(0xFFFFFFFF) == -1
    assert sign_extend(0xFFF, 12) == -1
    assert sign_extend(0x7FF, 12) == 2047
    print("utils OK")
