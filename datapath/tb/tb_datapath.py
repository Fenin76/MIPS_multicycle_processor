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
    dut.i_reset.value = 0

    #initialise the memory
    # Instruction memory
    dut.inst_data_mem.inst_mem[0].value = 0x8C220004  # lw $2,4($1)
    dut.inst_data_mem.inst_mem[1].value = 0x20030019  # addi $3, $0, 25
    dut.inst_data_mem.inst_mem[2].value = 0x2004001E  # addi $4, $0, 30
    dut.inst_data_mem.inst_mem[3].value = 0x00832822  # sub $5, $3, $4
    dut.inst_data_mem.inst_mem[4].value = 0x10C000FB  # branch to 256 check readdata of inst data  mem
    dut.inst_data_mem.inst_mem[5].value = 0xAC050404   #store value in reg 5 to mem location 257

    # Data memory 
    dut.inst_data_mem.data_mem[0].value = 0x08000005 #jump to addr 5

    await RisingEdge(dut.i_clk)
    await Timer(3, unit="ps")
    cocotb.log.info(f"new mem value is {dut.inst_data_mem.inst_mem[0].value}")

    #initialise fetch in next edge load
    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 1
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 1
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 1

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 3
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 1
    dut.i_alusrcb.value = 2
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 1
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 0
    dut.i_aluctrl.value = 0
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    #starting operation of load word write  back
    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 0
    dut.i_aluctrl.value = 0
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0
    dut.i_regdst.value = 0
    dut.i_regwrite.value = 1
    dut.i_memtoreg.value = 1
    
    #initialise fetch in next edge addi
    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 1
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 1
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 1
    dut.i_regdst.value = 0
    dut.i_regwrite.value = 0
    dut.i_memtoreg.value = 0

    #need to wait ome ps to update value
    await Timer(1, unit="ps")
    assert dut.reg_unit.internal_reg_file[2].value == 0x20030019, f"error in reg value expected 0x20030019, recieved {dut.reg_unit.internal_reg_file[2].value}"

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 3
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 1
    dut.i_alusrcb.value = 2
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 0
    dut.i_aluctrl.value = 0
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0
    dut.i_regdst.value = 0
    dut.i_regwrite.value =  1
    dut.i_memtoreg.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 1
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 1
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 1
    dut.i_regdst.value = 0
    dut.i_regwrite.value = 0
    dut.i_memtoreg.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 3
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 1
    dut.i_alusrcb.value = 2
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 0
    dut.i_aluctrl.value = 0
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0
    dut.i_regdst.value = 0
    dut.i_regwrite.value =  1
    dut.i_memtoreg.value = 0

    #new inst subtraction rtype
    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 1
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 1
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 1
    dut.i_regdst.value = 0
    dut.i_regwrite.value = 0
    dut.i_memtoreg.value = 0

    #1 ps delay needed
    await Timer(1, unit="ps")
    assert dut.reg_unit.internal_reg_file[3].value == 25, f"error in reg value expected 25, recieved {dut.reg_unit.internal_reg_file[3].value}"
    assert dut.reg_unit.internal_reg_file[4].value == 30, f"error in reg value expected 30, recieved {dut.reg_unit.internal_reg_file[3].value}"

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 3
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk) #subtract
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 1
    dut.i_alusrcb.value = 0
    dut.i_aluctrl.value = 6
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk) #writeback
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 0
    dut.i_aluctrl.value = 0
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0
    dut.i_regdst.value = 1
    dut.i_memtoreg.value = 0
    dut.i_regwrite.value = 1

    #beqinstruction
    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 1
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 1
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 1
    dut.i_regdst.value = 0
    dut.i_regwrite.value = 0
    dut.i_memtoreg.value = 0
    await Timer(1, unit="ps")
    assert dut.reg_unit.internal_reg_file[5].value == 5, f"error in reg value expected 5, recieved {dut.reg_unit.internal_reg_file[5].value}"

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 3
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk) #subtract
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 1
    dut.i_alusrcb.value = 0
    dut.i_aluctrl.value = 6
    dut.i_pcsrc.value = 1
    dut.i_branch.value  = 1
    dut.i_pcwrite.value = 0
    
    #for jump ---> fetch
    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 1
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 1
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 1
    dut.i_regdst.value = 0
    dut.i_regwrite.value = 0
    dut.i_memtoreg.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 3
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0
    assert dut.instr.value == 0x10C000FB, f"error in value, recieved {dut.instr.value}"
     

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 0
    dut.i_aluctrl.value = 0
    dut.i_pcsrc.value = 2
    dut.i_pcwrite.value = 1
   
    #------------>store word instruction
    #initialise fetch in next edge load
    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 1
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 1
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 1

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 3
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0
    assert dut.instr.value == 0x8000005, f"error in reading, recieved {dut.instr.value}"

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 0
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 1
    dut.i_alusrcb.value = 2
    dut.i_aluctrl.value = 2
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0

    await RisingEdge(dut.i_clk)
    dut.i_iord.value = 1
    dut.i_irwrite.value = 0
    dut.i_alusrca.value = 0
    dut.i_alusrcb.value = 0
    dut.i_aluctrl.value = 0
    dut.i_pcsrc.value = 0
    dut.i_pcwrite.value = 0
    dut.i_memwrite.value = 1

    
    for _ in range(10):
        await Timer(2, unit="ns")

    #write the values to a file
    await RisingEdge(dut.i_clk)
    with open("memory_dump.txt", "w") as f:
        for i in range(len(dut.inst_data_mem.inst_mem) - 150):
            value = int(dut.inst_data_mem.inst_mem[i].value)  # get memory content
            f.write(f"{i:04d}: {value:08X}\n")  # write index and value in hex
        
        for i in range(len(dut.inst_data_mem.data_mem)-200):
            value = int(dut.inst_data_mem.data_mem[i].value)  # get memory content
            f.write(f"{i:04d}: {value:08X}\n")  # write index and value in hex

  


