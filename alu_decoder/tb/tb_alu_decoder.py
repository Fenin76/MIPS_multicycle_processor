import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def tb_alu_decorder(dut):
    #initialise
    dut.i_aluop.value = 0
    dut.i_funct.value = 0
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 2, F"Error expected 2 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check aluop 01
    dut.i_aluop.value = 1
    dut.i_funct.value = 32
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 6, F"Error expected 6 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check funct and
    dut.i_aluop.value = 3
    dut.i_funct.value = 0x24
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() ==0, F"Error expected 0 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check funct OR
    dut.i_aluop.value = 3
    dut.i_funct.value = 0x25
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 1, F"Error expected 1 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check funct add
    dut.i_aluop.value = 3
    dut.i_funct.value = 0x20
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 2, F"Error expected 2 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check funct NOR
    dut.i_aluop.value = 3
    dut.i_funct.value = 0x27
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 4, F"Error expected 4 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check aluop 00
    dut.i_aluop.value = 0
    dut.i_funct.value = 0x24
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 2, F"Error expected 2 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check funct xOR
    dut.i_aluop.value = 3
    dut.i_funct.value = 0x26
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 5, F"Error expected 5 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check funct sub
    dut.i_aluop.value = 3
    dut.i_funct.value = 0x22
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 6, F"Error expected 6 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check funct slt
    dut.i_aluop.value = 3
    dut.i_funct.value = 0x2A
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 7, F"Error expected 7 recievd {dut.o_aluctrl.value.to_unsigned()}"

    #check funct nop
    dut.i_aluop.value = 3
    dut.i_funct.value = 0x2F
    await Timer(1, unit='ns')
    assert dut.o_aluctrl.value.to_unsigned() == 3, F"Error expected 3 recievd {dut.o_aluctrl.value.to_unsigned()}"

    for _ in range(2):
        await Timer(1, unit='ns')






