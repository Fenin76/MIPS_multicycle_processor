`timescale 1ns / 1ps

module datapath(i_clk,
                i_iord,
                i_memwrite,
                i_irwrite,
                i_regdst,
                i_memtoreg,
                i_regwrite,
                i_alusrca,
                i_alusrcb,
                i_aluctrl,
                i_pcsrc,
                i_branch,
                i_pcwrite,
                i_reset,
                o_operand,
                o_func);

input i_clk;

input i_iord;
input i_memwrite;
input i_irwrite;

input i_regdst;
input i_memtoreg;
input i_regwrite;

input i_alusrca;
input [1:0] i_alusrcb;
input [2:0] i_aluctrl;

input [1:0] i_pcsrc;
input i_branch;
input i_pcwrite;

input i_reset;

output wire [5:0] o_operand;
output wire [5:0]  o_func;


wire [31:0] pc_value;
wire [31:0] alu_out;
wire [31:0] Adr;

wire [31:0] data;

wire [31:0] w_data;
wire [31:0] o_rdata;

wire [31:0] instr;

wire [4:0] address3;
wire [31:0] data3;

wire [31:0] data_a;
wire [31:0] data_b;

wire [31:0] o_data_a;
wire [31:0] o_data_b;

wire [31:0] signimm;

wire [31:0] shift_value;

wire [31:0] srca;

wire [31:0] srcb;

wire set_zero;
wire [31:0] alu_result;

wire res_branch;

wire pc_en;

wire [27:0] jump_value;

wire [31:0] new_pcvalue;

//Pc register
dff_en pc_reg(.i_clk(i_clk), 
              .i_en(pc_en), 
              .i_reset(i_reset), 
              .i_data(new_pcvalue), 
              .o_data(pc_value));

//mux after PC
mux2x1 #(.width_a(32), .width_b(32), .width_c(32)) i_d_mux(.i_a(pc_value), 
                                                           .i_b(alu_out),
                                                           .o_c(Adr), 
                                                           .i_sel(i_iord));

//inst and data memory
inst_data_memory #(.depth_inst(256), .depth_data(256)) inst_data_mem(.i_clk(i_clk), 
                                                                     .i_addr(Adr), 
                                                                     .i_we(i_memwrite), 
                                                                     .i_wdata(o_data_b), 
                                                                     .o_rdata(o_rdata));

//DFF for instruction
dff_en inst_reg(.i_clk(i_clk), 
                .i_en(i_irwrite), 
                .i_reset(i_reset), 
                .i_data(o_rdata), 
                .o_data(instr));

//always enabled Data DFF
dff_en data_reg(.i_clk(i_clk), 
                .i_en(1'b1), 
                .i_reset(i_reset), 
                .i_data(o_rdata), 
                .o_data(data));

//register number rs. rt destination mux
mux2x1 #(.width_a(5), .width_b(5), .width_c(5)) regdst_mux(.i_a(instr[20:16]), 
                                                           .i_b(instr[15:11]), 
                                                           .o_c(address3), 
                                                           .i_sel(i_regdst));

//data mux alu, in sel mux
mux2x1 #(.width_a(32), .width_b(32), .width_c(32)) data_mux(.i_a(alu_out), 
                                                            .i_b(data), 
                                                            .o_c(data3), 
                                                            .i_sel(i_memtoreg));

//register unit of 32x32 register
register_file reg_unit(.i_clk(i_clk),
                       .i_a1(instr[25:21]),
                       .i_a2(instr[20:16]),
                       .i_a3(address3),
                       .i_wd3(data3),
                       .i_we3(i_regwrite),
                       .o_rd1(data_a),
                       .o_rd2(data_b));

//output a and b register to hold value originally 1 x 2in dff needed but we replace it 2 x 1in dff with same clock
//dff1
dff_en data_reg_a(.i_clk(i_clk), 
                 .i_en(1'b1), 
                 .i_reset(i_reset), 
                 .i_data(data_a), 
                 .o_data(o_data_a));

//dff2
dff_en data_reg_b(.i_clk(i_clk), 
                  .i_en(1'b1), 
                  .i_reset(i_reset), 
                  .i_data(data_b), 
                  .o_data(o_data_b));

//sign immedeate 
sign_imm sign_unit(.i_data(instr[15:0]),
                   .o_imm(signimm));

//multiplier
mul4 #(.width_in(32), .width_out(32)) shift2_pc(.i_data(signimm),
                                                .o_data(shift_value));

//ssource a mux
mux2x1 #(.width_a(32), .width_b(32), .width_c(32)) mux_a(.i_a(pc_value), 
                                                         .i_b(o_data_a), 
                                                         .o_c(srca), 
                                                         .i_sel(i_alusrca));

//source b mux
mux4x1 #(.data_width(32)) mux_b(.i_a(o_data_b),
                                .i_b(32'd4),
                                .i_c(signimm),
                                .i_d(shift_value),
                                .o_data(srcb),
                                .i_sel(i_alusrcb));

alu #(.DATA_WIDTH(32), .OP_WIDTH(3)) alu_i(.i_in1(srca),
                                           .i_in2(srcb),
                                           .i_op(i_aluctrl),
                                           .o_zero(set_zero),
                                           .o_data(alu_result));

and branch_and(res_branch, set_zero, i_branch);
or pcwrite_or(pc_en, res_branch, i_pcwrite);

dff_en alu_reg(.i_clk(i_clk), 
               .i_en(1'b1), 
               .i_reset(i_reset), 
               .i_data(alu_result), 
               .o_data(alu_out));

mul4 #(.width_in(26), .width_out(28)) shift2_jump(.i_data(instr[25:0]),
                                                  .o_data(jump_value));

mux4x1 #(.data_width(32)) mux_pc(.i_a(alu_result),
                                  .i_b(alu_out),
                                  .i_c({pc_value[31:28], jump_value}),
                                  .i_d(32'b1),
                                  .o_data(new_pcvalue),
                                  .i_sel(i_pcsrc));


assign o_operand = instr[31:26];
assign o_func = instr[5:0];

endmodule

