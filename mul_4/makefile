SIM ?= verilator

TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES = rtl/mul4.v

TOPLEVEL = mul4

# MODULE is the basename of the Python test file
COCOTB_TEST_MODULES = tb.tb_mul4

EXTRA_ARGS += --trace --trace-structs --timescale 1ns/1ps --coverage

WAVES = 1

# Set timescale for simulation
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

SIM_BUILD = sim_build

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim