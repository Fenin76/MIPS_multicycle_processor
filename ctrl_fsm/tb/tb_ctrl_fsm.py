import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

async def test_state(dut, opcode, expected_states):
    dut.i_opcode.value = opcode
    cocotb.log.info(f"the opcode is {opcode}")
    for expected in expected_states:
        await RisingEdge(dut.i_clk)
        dut._log.info(f"FSM current_state = {int(dut.current_state.value)}, expected = {expected}")
        if dut.current_state.value != expected:
            dut._log.error(f"FSM state mismatch! Got {dut.current_state.value}, expected {expected}")


@cocotb.test()
async def tb_register_file(dut):
    """Simple test for ctrlfsm"""
    cocotb.log.info("Starting test")

    # Start clock (10ns period = 100MHz)
    clock = Clock(dut.i_clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    cocotb.log.info("Clock started")
    
    dut.i_reset.value = 1
    await Timer(2, unit="ns")
    await RisingEdge(dut.i_clk)

    
    dut.i_reset.value = 0
    await RisingEdge(dut.i_clk)


    #load word
    await test_state(dut, 0x23, [0,1,2,3,4,0])

    # Store Word (SW)
    await test_state(dut, 0x2B, [1,2,5,0])

    # R-type
    await test_state(dut, 0x00, [1,6,7,0])

    # ADDI
    await test_state(dut, 0x08, [1,9,10,0])

    # BEQ
    await test_state(dut, 0x04, [1,8,0])

    # JUMP
    await test_state(dut, 0x02, [1,11,0])

    dut._log.info("FSM test completed")
    

    
    