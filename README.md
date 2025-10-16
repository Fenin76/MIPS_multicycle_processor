#MIPS_processor

A 32-bit multi-cycle MIPS processor implemented in RTL. Currently non-pipelined, with plans to add pipelining in the future. Designed for educational and verification purposes using Verilator and Cocotb.

Features

32-bit MIPS instruction set (subset)

R-type: add, sub, and, or, xor, nor, slt

I-type: addi, andi, ori, lw, sw, beq

J-type: j

Multi-cycle datapath

Testbench support with Cocotb for verification

Internal instruction and data memory (self-contained)

Easy to extend with pipelining in the future

Future-proof for memory-mapped I/O

Requirements

Verilator – for RTL simulation and waveform generation

Cocotb – Python-based testbench framework

Python 3.x for Cocotb tests



Directory Structure (example)
MIPS_processor/
├── rtl/             # RTL source files
├── tb/              # Testbench (Cocotb)
├── sim/             # Simulation scripts
├── waveform/        # waveform
├── README.md

Quick Start

Install dependencies

sudo apt install verilator
pip install cocotb


Simulate with Verilator + Cocotb

make sim


Run testbench

make tb

Usage

Load your instructions into inst_mem for simulation.

Internal memory values can be checked via testbench.

External I/O can be added in the future via memory-mapped addresses.

Future Work

Add pipelining to increase throughput

Support memory-mapped I/O for connecting to peripherals

Integrate with OpenLane flow for ASIC implementation
