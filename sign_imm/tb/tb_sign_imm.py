import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_basic_si(dut):
    #initialisation of the system
    dut.i_data.value = 0
    await Timer(1, unit="ns")
    assert dut.o_imm.value.to_unsigned() == 0, f"got {dut.o_imm.value.to_register} , expected 0"
    
    dut.i_data.value = -255
    await Timer(1, unit="ns")
    assert dut.o_imm.value.to_unsigned() == 4294967041, f"got {dut.o_imm.value.to_register} , expected 4294967041"

    dut.i_data.value = 10
    await Timer(1, unit="ns")
    assert dut.o_imm.value.to_unsigned() == 10, f"got {dut.o_imm.value.to_register} , expected 10"

    dut.i_data.value = 65000
    await Timer(1, unit="ns")
    assert dut.o_imm.value.to_unsigned() == 4294966760, f"got {dut.o_imm.value.to_register} , expected 4294966760"
    
    dut.i_data.value = -32768
    await Timer(1, unit="ns")
    assert dut.o_imm.value.to_unsigned() == 4294934528, f"got {dut.o_imm.value.to_register} , expected 4294934528"
    
    for _ in range(1):
        await Timer(5, unit="ns")

