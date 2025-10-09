`timescale 1ns / 1ps
module mul4(i_data,
            o_data);

parameter width_in = 32;
parameter width_out = 32;

input [width_in-1:0] i_data;
output wire [width_out-1:0] o_data;

assign o_data = i_data<<2;

endmodule
