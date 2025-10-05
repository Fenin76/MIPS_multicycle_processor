`timescale 1ns / 1ps
module mux2x1(i_a,
              i_b,
              i_sel,
              o_c);

parameter width_a = 32;
parameter width_b = 32;
parameter width_c = 32;

input [width_a-1:0] i_a;
input [width_b-1:0] i_b;
input i_sel;

output wire [width_c-1:0] o_c;

assign o_c = i_sel ? i_b : i_a;

endmodule
