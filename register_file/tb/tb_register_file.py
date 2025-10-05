import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def tb_register_file(dut):
    """Simple write and read test for the register file"""
    cocotb.log.info("Starting test")

    # Start clock (10ns period = 100MHz)
    clock = Clock(dut.i_clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    cocotb.log.info("Clock started")

    # Initialize inputs
    dut.i_we3.value = 0
    dut.i_a1.value = 0
    dut.i_a2.value = 0
    dut.i_a3.value = 0
    dut.i_wd3.value = 0
    cocotb.log.info("Inputs initialized")

    # Wait for one clock cycle to stabilize
    await RisingEdge(dut.i_clk)
    cocotb.log.info("First clock edge")

    # Write 42 into register 1
    dut.i_a3.value = 0
    dut.i_wd3.value = 42
    dut.i_we3.value = 1
    await RisingEdge(dut.i_clk)  # Wait for write to happen
    dut.i_we3.value = 0
    cocotb.log.info("Wrote 42 to register 0")

    #wait for 2 ns to write new value
    await Timer(2, unit="ns")
    await RisingEdge(dut.i_clk)
    dut.i_a3.value = 1
    dut.i_wd3.value = 30
    dut.i_we3.value = 1
    await RisingEdge(dut.i_clk)
    dut.i_we3.value = 0
    cocotb.log.info("wrote 30 to register 1")


    # Read back from register 0 and 1 at same time
    dut.i_a1.value = 0
    dut.i_a2.value = 1
    await RisingEdge(dut.i_clk)  # Wait for output to update
    cocotb.log.info(f"Read o_rd1: {dut.o_rd1.value.to_unsigned()}")
    cocotb.log.info(f"Read o_rd2: {dut.o_rd2.value.to_unsigned()}")
    assert dut.o_rd1.value.to_unsigned() == 42, f"Read {dut.o_rd1.value.to_unsigned()}, expected 42"
    assert dut.o_rd2.value.to_unsigned() == 30, f"Read {dut.o_rd2.value.to_unsigned()}, expected 30"

    # Optionally read another register
    dut.i_a2.value = 2
    await RisingEdge(dut.i_clk)
    cocotb.log.info(f"Read o_rd2: {dut.o_rd2.value.to_unsigned()}")
    assert dut.o_rd2.value.to_unsigned() == 0, f"Read {dut.o_rd2.value.to_unsigned()}, expected 0"
