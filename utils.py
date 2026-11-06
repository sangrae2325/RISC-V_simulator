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
    raise NotImplementedError("TODO(B): to_u32")


def to_signed(x: int) -> int:
    """32비트 값을 부호 있는 정수로 해석한다. (blt, bge에서 사용)

    예) to_signed(0xFFFFFFFF) == -1, to_signed(1) == 1
    """
    raise NotImplementedError("TODO(B): to_signed")


def sign_extend(value: int, bits: int) -> int:
    """bits 비트짜리 value를 부호 확장한다. 최상위 비트가 1이면 음수로.

    반환값은 파이썬 int(음수 가능). 레지스터에 넣을 때는 set_reg가 to_u32 한다.
    예) sign_extend(0xFFF, 12) == -1, sign_extend(0x7FF, 12) == 2047
    """
    raise NotImplementedError("TODO(B): sign_extend")


if __name__ == "__main__":
    # python utils.py 로 단독 확인
    assert to_u32(-1) == 0xFFFFFFFF
    assert to_signed(0xFFFFFFFF) == -1
    assert sign_extend(0xFFF, 12) == -1
    assert sign_extend(0x7FF, 12) == 2047
    print("utils OK")
