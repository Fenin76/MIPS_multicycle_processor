`timescale 1ns / 1ps

module alu_decoder(i_aluop,
                   i_funct,
                   o_aluctrl);

input [1:0] i_aluop;
input [5:0] i_funct;

output reg [2:0] o_aluctrl;

parameter AND  = 3'b000;
parameter OR   = 3'b001;
parameter ADD  = 3'b010;
parameter NOP  = 3'b011;
parameter NOR = 3'b100;
parameter XOR  = 3'b101;
parameter SUB  = 3'b110;
parameter SLT  = 3'b111;


always @ (*) begin
    if(i_aluop == 2'b10) begin
        case(i_funct) 
        6'b100000 : o_aluctrl = ADD;
        6'b100010 : o_aluctrl = SUB;
        6'b100100 : o_aluctrl = AND;
        6'b100101 : o_aluctrl = OR;
        6'b101010 : o_aluctrl = SLT;
        6'b100110 : o_aluctrl = XOR;
        6'b100111 : o_aluctrl = NOR; 
        default : o_aluctrl = NOP;
        endcase
    end else begin
        o_aluctrl = (i_aluop == 2'b00) ? ADD : (i_aluop == 2'b01) ? SUB : NOP;

    end

end

endmodule

