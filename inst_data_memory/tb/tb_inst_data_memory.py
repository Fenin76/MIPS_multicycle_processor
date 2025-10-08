import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ReadOnly



@cocotb.test()
async def tb_inst_data_memory(dut):
    cocotb.log.info("Starting test")

    # Start clock (10ns period = 100MHz)
    clock = Clock(dut.i_clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    cocotb.log.info("Clock started")

    try:
        #initialise
        with open("program.hex") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            line = line.strip()  # remove spaces, tabs, newlines
            if not line:  # skip blank lines
                continue
            value = int(line, 16)
            dut.inst_mem[i].value = value

        await RisingEdge(dut.i_clk)
        cocotb.log.info("Memory initialized from program.hex")
    except:
        cocotb.log.info("Memory is not initialized from program.hex")

    await RisingEdge(dut.i_clk)
    await ReadOnly()
    assert dut.inst_mem[0].value.to_unsigned() == 537395205, f"Read {dut.inst_mem[0].value.to_unsigned()}, expected 537395205"


    await RisingEdge(dut.i_clk)
    dut.i_addr.value = 4
    await RisingEdge(dut.i_clk)
    await ReadOnly()
    assert dut.inst_mem[1].value.to_unsigned() == 537460739, f"Read {dut.inst_mem[0].value.to_unsigned()}, expected 537460739"
    assert dut.o_rdata.value.to_unsigned()==537460739, f"Read { dut.o_rdata.value.to_unsigned()}, expected 537460739"


    await RisingEdge(dut.i_clk)
    dut.i_addr.value = 12
    dut.i_we.value = 1
    dut.i_wdata.value = 20465783

    await RisingEdge(dut.i_clk)
    dut.i_addr.value = 1200
    dut.i_we.value = 1
    dut.i_wdata.value = 1

    await RisingEdge(dut.i_clk)
    dut.i_addr.value = 12
    dut.i_we.value = 0
    await ReadOnly()

    async def test_inst_mem():
        assert dut.inst_mem[3].value.to_unsigned() == 20465783, f"Read {dut.inst_mem[10].value.to_unsigned()}, expected 20465783"
        cocotb.log.info("done inst testing")
    
    async def test_data_mem():
        assert dut.data_mem[44].value.to_unsigned() == 1, f"Read {dut.data_mem[44].value.to_unsigned()}, expected 1"
        cocotb.log.info("done data testing")

    async def test_read_inst_mem():
        assert dut.o_rdata.value.to_unsigned() == 20465783, f"Read {dut.o_rdata.value.to_unsigned()}, expected 20465783"


    await cocotb.start_soon(test_inst_mem())
    await cocotb.start_soon(test_inst_mem())
    await cocotb.start_soon(test_read_inst_mem())

    await RisingEdge(dut.i_clk)
    dut.i_addr.value = 12
    dut.i_we.value = 0
    assert dut.o_rdata.value.to_unsigned() == 20465783, f"Read {dut.o_rdata.value.to_unsigned()}, expected 20465783"

    dut.i_addr.value = 1200
    dut.i_we.value = 0
    await Timer(20, unit = "ps")
    assert dut.o_rdata.value.to_unsigned() == 1, f"Read {dut.o_rdata.value.to_unsigned()}, expected 1"


    for _ in range(200):
        await RisingEdge(dut.i_clk)

    
