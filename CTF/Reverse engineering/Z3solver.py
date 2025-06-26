import ctypes
from z3 import *
SECRET_VALUE = 315525
LEN = 30 
def solve_c_program():
    s = Solver()
    str_vars = [BitVec(f's_{i}', 8) for i in range(LEN)]
    for i in range(LEN - 1):
        s.add(str_vars[i] >= 32)  
        s.add(str_vars[i] <= 126)
    s.add(str_vars[LEN - 1] == 0)
    val = BitVecVal(0, 32)
    for i in range(LEN):
        currentbv = ZeroExt(24, str_vars[i])
        idx_bv = BitVecVal(i, 32)
        term1 = currentbv * currentbv
        term2 = currentbv * (BitVecVal(100, 32) - idx_bv)
        term3 = idx_bv
        term4 = currentbv * BitVecVal(7, 32)
        term5 = (currentbv | idx_bv) & (idx_bv + BitVecVal(3, 32))
        add_part = term1 + term2 + term3 + term4 + term5
        sub_part = URem(currentbv * currentbv, idx_bv + BitVecVal(1, 32))
        val = val + add_part - sub_part
    s.add(val == BitVecVal(SECRET_VALUE, 32))
    if s.check() == sat:
        m = s.model()
        found_string = ""
        for i in range(LEN):
            char_val = m[str_vars[i]].as_long()
            if i == LEN - 1 and char_val == 0:
                break
            found_string += chr(char_val)
        return found_string, m
    else:
        return None, None

def verify_string(input_str_from_z3):
    c_val = ctypes.c_int32(0)
    for i in range(LEN):
        current_char = 0
        if i < len(input_str_from_z3):
            current_char = ord(input_str_from_z3[i])
        term1_c = ctypes.c_int32(current_char * current_char)
        term2_c = ctypes.c_int32(current_char * (100 - i))
        term3_c = ctypes.c_int32(i)
        term4_c = ctypes.c_int32(current_char * 7)
        term5_c = ctypes.c_int32((current_char | i) & (i + 3))
        add_part_c = ctypes.c_int32(term1_c.value + term2_c.value + term3_c.value + term4_c.value + term5_c.value)
        sub_part_c = ctypes.c_int32((current_char * current_char) % (i + 1))
        c_val.value += (add_part_c.value - sub_part_c.value)
    return c_val.value

if __name__ == "__main__":
    found_string, model = solve_c_program()

    if found_string is not None:
        print(f"'{found_string}'")
        verified_val = verify_string(found_string)

    else:
        print("No solution found")


