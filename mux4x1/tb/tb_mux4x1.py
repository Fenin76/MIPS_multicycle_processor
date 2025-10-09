import cocotb
from cocotb.triggers import Timer

async def run_subtest(dut, a, b, c, d, sel, expected, delay_ns=10):
    dut.i_a.value = a
    dut.i_b.value = b
    dut.i_c.value = c
    dut.i_d.value = d
    dut.i_sel.value = sel
    await Timer(delay_ns, unit="ns")
    assert dut.o_data.value == expected, f"Expected {expected}, got {dut.o_data.value}"

@cocotb.test()
async def all_tests(dut):
    await run_subtest(dut, 10, 20, 25, 30, 0, 10)
    await run_subtest(dut, 10, 20, 1, 20, 1, 20)
    await run_subtest(dut, 33, 47, 0, 33, 2, 0)
    await run_subtest(dut, 11,  0, 1,  0, 3, 0)
    await run_subtest(dut, 1234556, 40, 0, 123455698, 1, 40)
    await run_subtest(dut, 4294967295, 4294967290, 1, 4294967295, 3, 4294967295)
    await run_subtest(dut, 10, 4, 0, 33, 2, 0)
    await run_subtest(dut, 11,  21, 31,  40, 3, 40)
    await run_subtest(dut, 1234556, 40, 11111111, 123455698, 1, 40)
    await run_subtest(dut, 4294967295, 4294967290, 1, 4294967295, 2, 1)
    
    #for extending tthe dump.vcd
    for _ in range(5):
        await Timer(10, unit="ns")