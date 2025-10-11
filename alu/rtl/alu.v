`timescale 1ns / 1ps

module alu(i_in1,
           i_in2,
           i_op,
           o_zero,
           o_data);

parameter DATA_WIDTH = 32;
parameter OP_WIDTH = 3;

parameter AND  = 3'b000;
parameter OR   = 3'b001;
parameter ADD  = 3'b010;
parameter NOP  = 3'b011;
parameter NOR = 3'b100;
parameter XOR  = 3'b101;
parameter SUB  = 3'b110;
parameter SLT  = 3'b111;

input [DATA_WIDTH-1:0] i_in1;
input [DATA_WIDTH-1:0] i_in2;
input [OP_WIDTH-1:0] i_op;

output reg [DATA_WIDTH-1:0] o_data;
output wire o_zero;

always @ (*) begin
    case(i_op)
    AND   : o_data = i_in1 & i_in2;
    OR    : o_data = i_in1 | i_in2;
    ADD   : o_data = i_in1 + i_in2;
    NOP   : o_data = 32'b0;
    NOR   : o_data = ~(i_in1|i_in2);
    XOR   : o_data = i_in1 ^ i_in2;
    SUB   : o_data = i_in1 - i_in2;
    SLT   : o_data = ($signed(i_in1) < $signed(i_in2)) ? {{(DATA_WIDTH-1){1'b0}},1'b1} : {DATA_WIDTH{1'b0}};
    default : o_data = 32'b0;
    endcase
end

assign o_zero = (o_data == 32'b0 )? 1'b1 : 1'b0; 

endmodule