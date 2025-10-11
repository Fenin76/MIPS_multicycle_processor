import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def run_alu_test(dut):
    #initialise
    dut.i_in1.value = 0
    dut.i_in2.value = 0
    dut.i_op.value  = 0
    await Timer(1, unit="ns")
    assert dut.o_data.value.to_unsigned() == 0, f"got {dut.o_data.value.to_unsigned()}, expected 0"
    assert bool(dut.o_zero.value) == 1, f"got {bool(dut.o_zero.value)}, expected 1"

    dut.i_in1.value = 0
    dut.i_in2.value = 1
    dut.i_op.value  = 0
    await Timer(1, unit="ns")
    assert dut.o_data.value.to_unsigned() == 0, f"got {dut.o_data.value.to_unsigned()}, expected 0"
    assert bool(dut.o_zero.value) == 1, f"got {bool(dut.o_zero.value)}, expected 1"

    dut.i_in1.value = 0
    dut.i_in2.value = 1
    dut.i_op.value  = 1
    await Timer(1, unit="ns")
    assert dut.o_data.value.to_unsigned() == 1, f"got {dut.o_data.value.to_unsigned()}, expected 1"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"

    dut.i_in1.value = 0
    dut.i_in2.value = 1
    dut.i_op.value  = 2
    await Timer(1, unit="ns")
    assert dut.o_data.value.to_unsigned() == 1, f"got {dut.o_data.value.to_unsigned()}, expected 1"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"


    dut.i_in1.value = 0
    dut.i_in2.value = 1
    dut.i_op.value  = 4
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0xFFFFFFFE, f"got {hex(dut.o_data.value)}, expected 0xFFFF_FFFE"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"


    dut.i_in1.value = 0
    dut.i_in2.value = 1
    dut.i_op.value  = 5
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0x00000001, f"got {hex(dut.o_data.value)}, expected 0x0000_0001"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"

    dut.i_in1.value = 0
    dut.i_in2.value = 1
    dut.i_op.value  = 6
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0xFFFFFFFF, f"got {hex(dut.o_data.value)}, expected 0xFFFF_FFFF"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"

    dut.i_in1.value = 0
    dut.i_in2.value = 1
    dut.i_op.value  = 7
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0x00000001, f"got {hex(dut.o_data.value)}, expected 0x0000_0001"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"

    dut.i_in1.value = 1
    dut.i_in2.value = 0
    dut.i_op.value  = 7
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0x00000000, f"got {hex(dut.o_data.value)}, expected 0x0000_0000"
    assert bool(dut.o_zero.value) == 1, f"got {bool(dut.o_zero.value)}, expected 1"

    dut.i_in1.value = 0xFFFF_FFFF
    dut.i_in2.value = 0xFFFF_FFF3
    dut.i_op.value  = 7
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0x00000000, f"got {hex(dut.o_data.value)}, expected 0x0000_0000"
    assert bool(dut.o_zero.value) == 1, f"got {bool(dut.o_zero.value)}, expected 1"

    #overflow of 0x1FFFFFFF2
    dut.i_in1.value = 0xFFFF_FFFF
    dut.i_in2.value = 0xFFFF_FFF3
    dut.i_op.value  = 2
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0xFFFFFFF2, f"got {hex(dut.o_data.value)}, expected 0xFFFF_FFF2"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"

    
    dut.i_in1.value = 0xFFFF_FFFF
    dut.i_in2.value = 0xFFFF_FFF3
    dut.i_op.value  = 6
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0x0000000C, f"got {hex(dut.o_data.value)}, expected  0x0000000C"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"

    
    dut.i_in1.value = 0xFFFF_FFFF
    dut.i_in2.value = 0xFFFF_FFF3
    dut.i_op.value  = 0
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0xFFFF_FFF3, f"got {hex(dut.o_data.value)}, expected   0xFFFF_FFF3"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"

    dut.i_in1.value = 0xFFFF_FFFF
    dut.i_in2.value = 0xFFFF_FFF3
    dut.i_op.value  = 1
    await Timer(1, unit="ns")
    assert dut.o_data.value == 0xFFFF_FFFF, f"got {hex(dut.o_data.value)}, expected   0xFFFF_FFFF"
    assert bool(dut.o_zero.value) == 0, f"got {bool(dut.o_zero.value)}, expected 0"

    dut.i_in1.value = 0xFFFF_FFFF
    dut.i_in2.value = 0xFFFF_FFF3
    dut.i_op.value  = 3
    await Timer(1, unit="ns")
    assert dut.o_data.value.to_unsigned() == 0, f"got {hex(dut.o_data.value)}, expected   0"
    assert bool(dut.o_zero.value) == 1, f"got {bool(dut.o_zero.value)}, expected 1"



    for _ in range(2):
        await Timer(1, unit = "ns")