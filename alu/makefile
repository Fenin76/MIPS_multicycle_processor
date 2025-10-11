SIM ?= verilator

TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES = rtl/alu.v

TOPLEVEL = alu

# MODULE is the basename of the Python test file
MODULE = tb.tb_alu

EXTRA_ARGS += --trace --trace-structs --timescale 1ns/1ps --coverage

WAVES = 1

# Set timescale for simulation
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

SIM_BUILD = sim_build

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim