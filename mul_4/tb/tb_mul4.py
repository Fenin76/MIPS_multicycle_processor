import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def tb_mul4(dut):
    #first test
    dut.i_data.value = 0
    await Timer(1, unit="ns")
    assert dut.o_data.value.to_unsigned() == 0, f"got {dut.to_daa.value.to_unsigned()}, expected 0"

    #val
    dut.i_data.value = 5
    await Timer(1, unit="ns")
    assert dut.o_data.value.to_unsigned() == 20, f"got {dut.to_daa.value.to_unsigned()}, expected 20"

    #val
    dut.i_data.value = 1024
    await Timer(1, unit="ns")
    assert dut.o_data.value.to_unsigned() == 4096, f"got {dut.to_daa.value.to_unsigned()}, expected 4096"

    #val
    dut.i_data.value = 0xFFFFFFFF
    await Timer(1, unit="ns")
    assert dut.o_data.value.to_unsigned() == 4294967292, f"got {dut.to_daa.value.to_unsigned()}, expected 4294967292"

    #val
    dut.i_data.value = 0x200
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0x800, f"got {dut.to_daa.value}, expected 0x800"


    for _ in range(5):
        await Timer(1, unit="ns")
