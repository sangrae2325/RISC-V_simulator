"""decoder.py - 명령어 해독 (담당: C 보민)

decode(inst)의 반환 형식 (팀 공통 약속):
    지원 명령어  -> dict
        {
            "name": "add",   # add sub and or addi andi ori lui lw sw beq bne blt bge
            "rd": int,
            "rs1": int,
            "rs2": int,
            "imm": int,      # 부호 확장된 파이썬 int (음수 가능). 즉시값 없는 R형은 0
        }
    invalid      -> None
"""

from utils import sign_extend


def get_fields(inst: int) -> dict:
    """32비트 명령어에서 필드를 뽑는다.

    반환: {"opcode", "rd", "funct3", "rs1", "rs2", "funct7"}
      opcode = inst[6:0], rd = inst[11:7], funct3 = inst[14:12],
      rs1 = inst[19:15], rs2 = inst[24:20], funct7 = inst[31:25]
    """
    raise NotImplementedError("TODO(C): get_fields")


def imm_i(inst: int) -> int:
    """I형 즉시값: inst[31:20], 12비트 부호 확장"""
    raise NotImplementedError("TODO(C): imm_i")


def imm_s(inst: int) -> int:
    """S형 즉시값: inst[31:25] + inst[11:7], 12비트 부호 확장"""
    raise NotImplementedError("TODO(C): imm_s")


def imm_b(inst: int) -> int:
    """B형 즉시값: imm[12|10:5|4:1|11] 재조립, 13비트 부호 확장 (항상 짝수)"""
    raise NotImplementedError("TODO(C): imm_b")


def imm_u(inst: int) -> int:
    """U형 즉시값: inst & 0xFFFFF000"""
    raise NotImplementedError("TODO(C): imm_u")


def decode(inst: int):
    """opcode -> funct3 -> funct7 순서로 명령어를 판별한다.

    opcode 0x33 R형: add/sub(funct3=0, funct7=0x00/0x20), or(6), and(7)
    opcode 0x13 I형: addi(0), ori(6), andi(7)
    opcode 0x03 I형: lw(2)
    opcode 0x23 S형: sw(2)
    opcode 0x63 B형: beq(0), bne(1), blt(4), bge(5)
    opcode 0x37 U형: lui
    표에 없는 조합은 전부 None (invalid)
    """
    raise NotImplementedError("TODO(C): decode")


if __name__ == "__main__":
    # python decoder.py 로 단독 확인 (명세서 7절 예시)
    assert decode(0x100000b7)["name"] == "lui"
    assert decode(0x00700113)["name"] == "addi"
    assert decode(0x00310233)["name"] == "add"
    assert decode(0x0040a023)["name"] == "sw"
    assert decode(0x00000000) is None
    print("decoder OK")
