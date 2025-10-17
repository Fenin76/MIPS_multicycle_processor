import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def tb_datapath(dut):
    """Simple write and read test for the datapath"""
    cocotb.log.info("Starting test")

    # Start clock
    clock = Clock(dut.i_clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    cocotb.log.info("Clock started")

    # Apply reset
    dut.i_reset.value = 1
    await RisingEdge(dut.i_clk)

    # initialise the memory
    # Instruction memory
    dut.datapath_i.inst_data_mem.inst_mem[0].value  = 0x8C220004  # lw   $2, 4($1)        ; load word
    dut.datapath_i.inst_data_mem.inst_mem[1].value  = 0x20030019  # addi $3, $0, 25       ; $3 = 25
    dut.datapath_i.inst_data_mem.inst_mem[2].value  = 0x2004001E  # addi $4, $0, 30       ; $4 = 30

    # R-type operations 
    dut.datapath_i.inst_data_mem.inst_mem[3].value  = 0x00642822  # sub  $5,  $3, $4      ; $5 = $3 - $4
    dut.datapath_i.inst_data_mem.inst_mem[4].value  = 0x00643020  # add  $6,  $3, $4      ; $6 = $3 + $4
    dut.datapath_i.inst_data_mem.inst_mem[5].value  = 0x00643826  # xor  $7,  $3, $4      ; $7 = $3 ^ $4
    dut.datapath_i.inst_data_mem.inst_mem[6].value  = 0x00644025  # or   $8,  $3, $4      ; $8 = $3 | $4
    dut.datapath_i.inst_data_mem.inst_mem[7].value  = 0x00644824  # and  $9,  $3, $4      ; $9 = $3 & $4
    dut.datapath_i.inst_data_mem.inst_mem[8].value  = 0x00645027  # nor  $10, $3, $4      ; $10 = ~($3 | $4)
    dut.datapath_i.inst_data_mem.inst_mem[9].value  = 0x0064582A  # slt  $11, $3, $4      ; $11 = ($3 < $4) ? 1 : 0

    # example branch and store
    dut.datapath_i.inst_data_mem.inst_mem[10].value = 0x10C000FB  # beq  $6, $0, offset   ; check branch encoding 
    dut.datapath_i.inst_data_mem.inst_mem[11].value = 0xAC050404  # sw   $5, 0x0404($0)   ; store $5 to data_mem[257] 

    dut.datapath_i.inst_data_mem.data_mem[0].value = 0x08000005  # 0x08000005 is 'j 0x00000005'

    await RisingEdge(dut.i_clk)
    await Timer(3, unit="ps")
    cocotb.log.info(f"new mem value is {dut.datapath_i.inst_data_mem.inst_mem[0].value}")
    dut.i_reset.value = 0

    for _ in range(50):
        await RisingEdge(dut.i_clk)

     # Example: read registers $3..$11 and check expected values
    expected = {
        3: 25,
        4: 30,
        5: 25 - 30,   # sub
        6: 25 + 30,   # add
        7: 25 ^ 30,      # xor result as example
        8: 25 | 30,      # or
        9: 25 & 30,      # and
        10: ~(25 | 30),     # nor
        11: 1         # slt -> 25 < 30 => 1
    }

    def to_signed(val, bits=32):
        val = int(val)
        if val & (1 << (bits - 1)):
            val -= 1 << bits
        return val

    for reg_num, exp in expected.items():
        reg_signal = dut.datapath_i.reg_unit.internal_reg_file[reg_num]
        value = to_signed(reg_signal.value)
        if exp is not None:
            assert value == exp, f"Reg {reg_num} = {value}, expected {exp}"
        else:
            dut._log.info(f"Reg ${reg_num} = {value}")

  
    data_word = int(dut.datapath_i.inst_data_mem.data_mem[0].value)
    dut._log.info(f"data_mem[0] = 0x{data_word:08x}")

    for _ in range(10):
        await Timer(2, unit="ns")

    #write the values to a file
    await RisingEdge(dut.i_clk)
    with open("memory_dump.txt", "w") as f:
        for i in range(len(dut.datapath_i.inst_data_mem.inst_mem) - 150):
            value = int(dut.datapath_i.inst_data_mem.inst_mem[i].value)  # get memory content
            f.write(f"{i:04d}: {value:08X}\n")  # write index and value in hex
        
        for i in range(len(dut.datapath_i.inst_data_mem.data_mem)-200):
            value = int(dut.datapath_i.inst_data_mem.data_mem[i].value)  # get memory content
            f.write(f"{i:04d}: {value:08X}\n")  # write index and value in hex
