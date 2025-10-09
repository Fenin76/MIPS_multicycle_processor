`timescale 1ns / 1ps

module mux4x1(i_sel,
              i_a,
              i_b,
              i_c,
              i_d,
              o_data);

parameter data_width = 32;

input [data_width-1 : 0] i_a;
input [data_width-1 : 0] i_b;
input [data_width-1 : 0] i_c;
input [data_width-1 : 0] i_d;
input [1:0] i_sel;

output reg [data_width-1 : 0] o_data;

always @ (*) begin
    case(i_sel) 
    2'b00 : o_data = i_a;
    2'b01 : o_data = i_b;
    2'b10 : o_data = i_c;
    2'b11 : o_data = i_d;
    default: o_data = 32'b0;
    endcase

end
endmodule
