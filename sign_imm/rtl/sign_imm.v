`timescale 1ns / 1ps


module sign_imm(i_data,
                o_imm);


input [15:0] i_data;

output wire [31:0] o_imm;

assign o_imm = {{16{i_data[15]}}, i_data};

endmodule

