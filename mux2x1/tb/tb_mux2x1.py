import cocotb
from cocotb.triggers import Timer

async def run_subtest(dut, a, b, sel, expected, delay_ns=10):
    dut.i_a.value = a
    dut.i_b.value = b
    dut.i_sel.value = sel
    await Timer(delay_ns, unit="ns")
    assert dut.o_c.value == expected, f"Expected {expected}, got {dut.o_c.value}"

@cocotb.test()
async def all_tests(dut):
    await run_subtest(dut, 10, 20, 0, 10)
    await run_subtest(dut, 10, 20, 1, 20)
    await run_subtest(dut, 30, 40, 0, 30)
    
    #for extending tthe dump.vcd
    for _ in range(5):
        await Timer(10, unit="ns")
