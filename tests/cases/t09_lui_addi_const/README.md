# t09_lui_addi_const

## 목적
lui+addi로 32비트 큰 상수 만들기: 음수 imm 보정(0xdeadbeef), 최상위 비트(0x80000000-1), 상위 전부 1(0xfffff000-1), lui가 하위 12비트를 0으로 덮어쓰는지

## 명령어

| 주소 | 기계어 | 어셈블리 |
| --- | --- | --- |
| 0x00040000 | 0x10000537 | lui x10, 0x10000 (x10 = 0x10000000) |
| 0x00040004 | 0x000010b7 | lui x1, 0x1 |
| 0x00040008 | 0x7ff08093 | addi x1, x1, 0x7ff (x1 = 0x000017ff, 양수 최대 imm) |
| 0x0004000c | 0x00152023 | sw x1, 0(x10) |
| 0x00040010 | 0xdeadc137 | lui x2, 0xdeadc |
| 0x00040014 | 0xeef10113 | addi x2, x2, -273 (x2 = 0xdeadbeef, 하위 12비트 0xeef가 음수라 상위 +1 보정) |
| 0x00040018 | 0x00252223 | sw x2, 4(x10) |
| 0x0004001c | 0x800001b7 | lui x3, 0x80000 (x3 = 0x80000000, 최상위 비트) |
| 0x00040020 | 0xfff18193 | addi x3, x3, -1 (x3 = 0x7fffffff) |
| 0x00040024 | 0x00352423 | sw x3, 8(x10) |
| 0x00040028 | 0xfffff237 | lui x4, 0xfffff (x4 = 0xfffff000) |
| 0x0004002c | 0xfff20213 | addi x4, x4, -1 (x4 = 0xffffefff) |
| 0x00040030 | 0x00452623 | sw x4, 12(x10) |
| 0x00040034 | 0x7ff00293 | addi x5, x0, 0x7ff (x5 = 0x7ff) |
| 0x00040038 | 0x000012b7 | lui x5, 0x1 (x5 = 0x00001000, 하위 12비트는 0으로 덮어씀) |
| 0x0004003c | 0x00552823 | sw x5, 16(x10) |
| 0x00040040 | 0x00000000 | invalid instruction (종료) |

## 초기 data.bin
0바이트

## 기대 결과 도출 근거

- 표준 출력: `PC 0x00040040 invalid instruction 0x00000000`
  - 분기 없는 직선 실행을 가정해, 마지막 단어의 주소와 값으로 계산했다.
- data.out 오프셋 0: `ff170000` (그 밖의 바이트는 data.bin 내용, 없으면 0)
- data.out 오프셋 4: `efbeadde` (그 밖의 바이트는 data.bin 내용, 없으면 0)
- data.out 오프셋 8: `ffffff7f` (그 밖의 바이트는 data.bin 내용, 없으면 0)
- data.out 오프셋 12: `ffefffff` (그 밖의 바이트는 data.bin 내용, 없으면 0)
- data.out 오프셋 16: `00100000` (그 밖의 바이트는 data.bin 내용, 없으면 0)
