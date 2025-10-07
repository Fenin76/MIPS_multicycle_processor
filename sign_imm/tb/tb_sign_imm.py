import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_basic_si(dut):
    #initialisation of the system
    dut.i_data.value = 0
    await Timer(1, unit="ns")

    dut.i_data.value = -255
    await Timer(1, unit="ns")

    dut.i_data.value = 10
    await Timer(1, unit="ns")

    dut.i_data.value = 65000
    await Timer(1, unit="ns")
    
    dut.i_data.value = -32768
    await Timer(1, unit="ns")
    
    for _ in range(1):
        await Timer(5, unit="ns")

