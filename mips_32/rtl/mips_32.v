`timescale 1ns / 1ps

module mips_32(i_clk,
               i_reset);

input i_clk;
input i_reset;

wire [5:0] i_opcode;

wire o_iord;
wire o_memwrite;
wire o_irwrite;
wire o_pcwrite;
wire o_branch;
wire [1:0] o_pcsrc;
wire o_regdst;
wire o_memtoreg;
wire [1:0] o_aluop;
wire o_alusrca;
wire [1:0] o_alusrcb;
wire o_regwrite;

wire [5:0] i_funct;
wire [2:0] o_aluctrl;

ctrl_fsm ctrl_fsm_i(.i_clk(i_clk), 
                    .i_reset(i_reset), 
                    .i_opcode(i_opcode),
                    .o_iord(o_iord),
                    .o_memwrite(o_memwrite), 
                    .o_irwrite(o_irwrite), 
                    .o_pcwrite(o_pcwrite),
                    .o_branch(o_branch),
                    .o_pcsrc(o_pcsrc),
                    .o_regdst(o_regdst),
                    .o_memtoreg(o_memtoreg),
                    .o_aluop(o_aluop),
                    .o_alusrca(o_alusrca),
                    .o_alusrcb(o_alusrcb),
                    .o_regwrite(o_regwrite));


alu_decoder alu_decoder_i(.i_aluop(o_aluop),
                            .i_funct(i_funct),
                            .o_aluctrl(o_aluctrl));


datapath datapath_i(.i_clk(i_clk),
                    .i_reset(i_reset),
                    .i_iord(o_iord),
                    .i_memwrite(o_memwrite),
                    .i_irwrite(o_irwrite),
                    .i_regdst(o_regdst),
                    .i_memtoreg(o_memtoreg),
                    .i_regwrite(o_regwrite),
                    .i_alusrca(o_alusrca),
                    .i_alusrcb(o_alusrcb),
                    .i_aluctrl(o_aluctrl),
                    .i_pcsrc(o_pcsrc),
                    .i_branch(o_branch),
                    .i_pcwrite(o_pcwrite),
                    .o_operand(i_opcode),
                    .o_func(i_funct));

endmodule
