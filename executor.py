"""executor.py - 명령어 실행 (담당: D 해인 / lw·sw는 B 진, execute는 공통)

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
    raise NotImplementedError("TODO(공통): execute")


# ---------------- D 해인 ----------------

def set_reg(regs: list, rd: int, value: int) -> None:
    """rd가 0이면 무시, 아니면 to_u32(value)를 저장한다."""
    raise NotImplementedError("TODO(D): set_reg")


def exec_r(d: dict, regs: list) -> None:
    """add, sub, and, or : rd = rs1 (op) rs2"""
    raise NotImplementedError("TODO(D): exec_r")


def exec_i(d: dict, regs: list) -> None:
    """addi, andi, ori : rd = rs1 (op) imm"""
    raise NotImplementedError("TODO(D): exec_i")


def exec_lui(d: dict, regs: list) -> None:
    """lui : rd = imm (imm_u 결과)"""
    raise NotImplementedError("TODO(D): exec_lui")


def exec_branch(d: dict, regs: list, pc: int) -> int:
    """beq, bne, blt, bge : 조건 참이면 pc + imm, 거짓이면 pc + 4 반환.

    blt, bge는 to_signed로 부호 비교. 반환값은 to_u32.
    """
    raise NotImplementedError("TODO(D): exec_branch")


# ---------------- B 진 ----------------

def exec_load(d: dict, regs: list, data_mem: bytearray) -> None:
    """lw : addr = to_u32(rs1 + imm), rd = read_word(data_mem, addr - DATA_START)"""
    raise NotImplementedError("TODO(B): exec_load")


def exec_store(d: dict, regs: list, data_mem: bytearray) -> None:
    """sw : addr = to_u32(rs1 + imm), write_word(data_mem, addr - DATA_START, rs2)"""
    raise NotImplementedError("TODO(B): exec_store")


if __name__ == "__main__":
    # python executor.py 로 단독 확인
    regs = [0] * 32
    set_reg(regs, 0, 123)
    assert regs[0] == 0
    set_reg(regs, 1, -1)
    assert regs[1] == 0xFFFFFFFF
    print("executor OK")
