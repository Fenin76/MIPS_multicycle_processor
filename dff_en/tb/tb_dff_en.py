import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ReadOnly

@cocotb.test()
async def tb_dff_en(dut):
    #start clock
    cocotb.log.info("Starting test")
    clock = Clock(dut.i_clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    cocotb.log.info("Starting clock")

    #initialise
    dut.i_reset.value = 1
    dut.i_en.value = 0
    dut.i_data.value = 100

    await RisingEdge(dut.i_clk)
    assert dut.o_data.value.to_unsigned() == 0, f"got {dut.o_data.value.to_unsigned()} expected 0"

    #change reset

    dut.i_reset.value = 0
    await RisingEdge(dut.i_clk)
    assert dut.o_data.value.to_unsigned() == 0, f"got {dut.o_data.value.to_unsigned()} expected 0"

    dut.i_en.value = 1
    await RisingEdge(dut.i_clk)
    assert dut.o_data.value.to_unsigned() == 0, f"got {dut.o_data.value.to_unsigned()} expected 0"

    dut.i_data.value = 250
    await RisingEdge(dut.i_clk)
    assert dut.o_data.value.to_unsigned() == 100, f"got {dut.o_data.value.to_unsigned()} expected 100"

    dut.i_en.value = 0
    dut.i_data.value = 100
    await RisingEdge(dut.i_clk)
    assert dut.o_data.value.to_unsigned() == 250, f"got {dut.o_data.value.to_unsigned()} expected 250"

    
    dut.i_en.value = 1
    dut.i_data.value = 100000
    await RisingEdge(dut.i_clk)
    assert dut.o_data.value.to_unsigned() == 250, f"got {dut.o_data.value.to_unsigned()} expected 250"
    
    await RisingEdge(dut.i_clk)
    assert dut.o_data.value.to_unsigned() == 100000, f"got {dut.o_data.value.to_unsigned()} expected 100000"

    await RisingEdge(dut.i_clk)
    dut.i_data.value = 4294967295
    await RisingEdge(dut.i_clk)
    await Timer(1, unit="ps")
    assert dut.o_data.value.to_unsigned() == 4294967295, f"got {dut.o_data.value.to_unsigned()} expected 4294967295"

    await RisingEdge(dut.i_clk)
    dut.i_data.value = 79797
    await RisingEdge(dut.i_clk)
    await Timer(1, unit="ps")
    assert dut.o_data.value.to_unsigned() == 79797, f"got {dut.o_data.value.to_unsigned()} expected 79797"


    for _ in range(3):
        await RisingEdge(dut.i_clk)




