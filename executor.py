"""executor.py - 명령어 실행 (담당: D 해인, execute는 공통)

- regs: 길이 32 리스트, 각 원소는 0 ~ 0xFFFFFFFF (항상 to_u32 된 값)
- d:    decoder.decode()가 반환한 dict
- 레지스터는 반드시 set_reg로만 바꾼다. (x0 고정)
"""

from utils import DATA_START, to_u32, to_signed
from memory import read_word, write_word


# ---------------- 공통 ----------------

def execute(d: dict, regs: list, data_mem: bytearray, pc: int) -> int:
    """d["name"]에 따라 아래 함수를 호출하고 다음 PC를 반환한다.

    분기는 exec_branch의 반환값, 나머지는 pc + 4.
    """
    if d["name"] in ["add", "sub", "and", "or"]:
        exec_r(d, regs)
    elif d["name"] in ["addi", "andi", "ori"]:
        exec_i(d, regs)
    elif d["name"] == "lui":
        exec_lui(d, regs)
    elif d["name"] in ["beq", "bne", "blt", "bge"]:
        return exec_branch(d, regs, pc)
    elif d["name"] == "lw":
        exec_load(d, regs, data_mem)
    elif d["name"] == "sw":
        exec_store(d, regs, data_mem)
    
    return to_u32(pc + 4)

# ---------------- D 해인 ----------------

def set_reg(regs: list, rd: int, value: int) -> None:
    """rd가 0이면 무시, 아니면 to_u32(value)를 저장한다."""
    
    if rd == 0 : 
        return 
    else : 
        regs[rd] = to_u32(value)


def exec_r(d: dict, regs: list) -> None:
    """add, sub, and, or : rd = rs1 (op) rs2"""
    
    if d["name"] == "add" : 
        set_reg(regs, d["rd"], to_u32(regs[d["rs1"]] + regs[d["rs2"]]))
    elif d["name"] == "sub" : 
        set_reg(regs, d["rd"], to_u32(regs[d["rs1"]] - regs[d["rs2"]]))
    elif d["name"] == "and" : 
        set_reg(regs, d["rd"], regs[d["rs1"]] & regs[d["rs2"]])
    elif d["name"] == "or" : 
        set_reg(regs, d["rd"], regs[d["rs1"]] | regs[d["rs2"]])

def exec_i(d: dict, regs: list) -> None:
    """addi, andi, ori : rd = rs1 (op) imm"""
    if d["name"] == "addi" :
        set_reg(regs, d["rd"], to_u32(regs[d["rs1"]] + d["imm"]))
    elif d["name"] == "andi" :
        set_reg(regs, d["rd"], regs[d["rs1"]] & d["imm"])
    elif d["name"] == "ori" : 
        set_reg(regs, d["rd"], regs[d["rs1"]] | d["imm"])
    
        

def exec_lui(d: dict, regs: list) -> None:
    """lui : rd = imm (imm_u 결과)"""
    set_reg(regs, d["rd"], d["imm"])

def exec_branch(d: dict, regs: list, pc: int) -> int:
    """beq, bne, blt, bge : 조건 참이면 pc + imm, 거짓이면 pc + 4 반환.

    blt, bge는 to_signed로 부호 비교. 반환값은 to_u32.
    """
    if d["name"] == "beq" : 
        if regs[d["rs1"]] == regs[d["rs2"]] : 
            return to_u32(pc + d["imm"])
        else : 
            return to_u32(pc + 4)
    elif d["name"] == "bne" : 
        if regs[d["rs1"]] != regs[d["rs2"]] : 
            return to_u32(pc + d["imm"])
        else : 
            return to_u32(pc + 4)
    elif d["name"] == "blt" : 
        if to_signed(regs[d["rs1"]]) < to_signed(regs[d["rs2"]]) : 
            return to_u32(pc + d["imm"])
        else : 
            return to_u32(pc + 4)
    elif d["name"] == "bge" : 
        if to_signed(regs[d["rs1"]]) >= to_signed(regs[d["rs2"]]) : 
            return to_u32(pc + d["imm"])
        else : 
            return to_u32(pc + 4)

# ---------------- D 해인 ----------------

def exec_load(d: dict, regs: list, data_mem: bytearray) -> None:
    """lw : addr = to_u32(rs1 + imm), rd = read_word(data_mem, addr - DATA_START)"""
    if d["name"] == "lw" :
        addr = to_u32(regs[d["rs1"]] + d["imm"])
        value = read_word(data_mem, addr - DATA_START)
        set_reg(regs, d["rd"], value)

def exec_store(d: dict, regs: list, data_mem: bytearray) -> None:
    """sw : addr = to_u32(rs1 + imm), write_word(data_mem, addr - DATA_START, rs2)"""
    if d["name"] == "sw" : 
        addr = to_u32(regs[d["rs1"]] + d["imm"])
        write_word(data_mem, addr - DATA_START, regs[d["rs2"]])

if __name__ == "__main__":
    # python executor.py 로 단독 확인
    regs = [0] * 32
    set_reg(regs, 0, 123)
    assert regs[0] == 0
    set_reg(regs, 1, -1)
    assert regs[1] == 0xFFFFFFFF
    print("executor OK")
