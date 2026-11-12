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
    inst &= 0xFFFFFFFF
    return {
        "opcode": inst & 0x7F,
        "rd": (inst >> 7) & 0x1F,
        "funct3": (inst >> 12) & 0x7,
        "rs1": (inst >> 15) & 0x1F,
        "rs2": (inst >> 20) & 0x1F,
        "funct7": (inst >> 25) & 0x7F,
    }


def imm_i(inst: int) -> int:
    """I형 즉시값: inst[31:20], 12비트 부호 확장"""
    return sign_extend((inst >> 20) & 0xFFF, 12)


def imm_s(inst: int) -> int:
    """S형 즉시값: inst[31:25] + inst[11:7], 12비트 부호 확장"""
    # inst[31:25]가 imm[11:5], inst[11:7]이 imm[4:0]
    value = (((inst >> 25) & 0x7F) << 5) | ((inst >> 7) & 0x1F)
    return sign_extend(value, 12)


def imm_b(inst: int) -> int:
    """B형 즉시값: imm[12|10:5|4:1|11] 재조립, 13비트 부호 확장 (항상 짝수)"""
    # inst[31]=imm[12], inst[7]=imm[11], inst[30:25]=imm[10:5], inst[11:8]=imm[4:1]
    # imm[0]은 항상 0
    value = (
        (((inst >> 31) & 0x1) << 12)
        | (((inst >> 7) & 0x1) << 11)
        | (((inst >> 25) & 0x3F) << 5)
        | (((inst >> 8) & 0xF) << 1)
    )
    return sign_extend(value, 13)


def imm_u(inst: int) -> int:
    """U형 즉시값: inst & 0xFFFFF000"""
    return inst & 0xFFFFF000


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
    inst &= 0xFFFFFFFF
    f = get_fields(inst)
    opcode, funct3, funct7 = f["opcode"], f["funct3"], f["funct7"]
    rd, rs1, rs2 = f["rd"], f["rs1"], f["rs2"]

    name = None
    imm = 0
    # 형식에 쓰이지 않는 필드는 0으로 둔다 (잘못 읽어도 영향이 없게)
    if opcode == 0x33:  # R형
        name = {
            (0, 0x00): "add",
            (0, 0x20): "sub",
            (6, 0x00): "or",
            (7, 0x00): "and",
        }.get((funct3, funct7))
    elif opcode == 0x13:  # I형 산술/논리
        name = {0: "addi", 6: "ori", 7: "andi"}.get(funct3)
        imm = imm_i(inst)
        rs2 = 0
    elif opcode == 0x03:  # I형 load
        name = "lw" if funct3 == 2 else None
        imm = imm_i(inst)
        rs2 = 0
    elif opcode == 0x23:  # S형
        name = "sw" if funct3 == 2 else None
        imm = imm_s(inst)
        rd = 0
    elif opcode == 0x63:  # B형
        name = {0: "beq", 1: "bne", 4: "blt", 5: "bge"}.get(funct3)
        imm = imm_b(inst)
        rd = 0
    elif opcode == 0x37:  # U형
        name = "lui"
        imm = imm_u(inst)
        rs1 = rs2 = 0

    if name is None:
        return None
    return {"name": name, "rd": rd, "rs1": rs1, "rs2": rs2, "imm": imm}


if __name__ == "__main__":
    # python decoder.py 로 단독 확인 (명세서 7절 예시)
    assert decode(0x100000b7)["name"] == "lui"
    assert decode(0x00700113)["name"] == "addi"
    assert decode(0x00310233)["name"] == "add"
    assert decode(0x0040a023)["name"] == "sw"
    assert decode(0x00000000) is None
    print("decoder OK")
