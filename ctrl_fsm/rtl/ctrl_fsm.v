`timescale  1ns / 1ps

module ctrl_fsm(i_clk,
                i_reset,
                i_opcode,
                o_iord,
                o_memwrite,
                o_irwrite,
                o_pcwrite,
                o_branch,
                o_pcsrc,
                o_regdst,
                o_memtoreg,
                o_aluop,
                o_alusrca,
                o_alusrcb,
                o_regwrite);

input i_clk;
input i_reset;
input [5:0] i_opcode;

output reg o_iord;
output reg o_memwrite;
output reg o_irwrite;
output reg o_pcwrite;
output reg o_branch;
output reg [1:0] o_pcsrc;
output reg o_regdst;
output reg o_memtoreg;
output reg [1:0] o_aluop;
output reg o_alusrca;
output reg [1:0] o_alusrcb;
output reg o_regwrite;

reg [3:0] current_state;
reg [3:0] next_state;

parameter IDLE = 4'b1100;
parameter FETCH = 4'b0000;
parameter DECODE = 4'b0001;
parameter MEM_ADR = 4'b0010;
parameter MEM_READ = 4'b0011;
parameter MEM_WB = 4'b0100;
parameter MEM_WRITE = 4'b0101;
parameter EXECUTE = 4'b0110;
parameter ALU_WB = 4'b0111;
parameter BRANCH = 4'b1000;
parameter I_EX = 4'b1001;
parameter I_WB = 4'b1010;
parameter JUMP = 4'b1011;

parameter RTYPE = 6'b000000;
parameter LW = 6'b100011;
parameter SW = 6'b101011;
parameter BEQ = 6'b000100;
parameter ADDI = 6'b001000;
parameter JMP = 6'b000010;

always @ (posedge i_clk) begin
  if (i_reset) begin
    current_state <= IDLE;
  end else begin
    current_state <= next_state;
  end
end

always @(*) begin
    o_iord = 1'b0;
    o_memwrite = 1'b0;
    o_irwrite = 1'b0;
    o_pcwrite = 1'b0;
    o_branch = 1'b0;
    o_pcsrc = 2'b00;
    o_regdst = 1'b0;
    o_memtoreg = 1'b0;
    o_aluop = 2'b00;
    o_alusrca = 1'b0;
    o_alusrcb = 2'b00;
    o_regwrite = 1'b0;
    case (current_state) 
        IDLE : begin
            o_iord = 1'b0;
            o_memwrite = 1'b0;
            o_irwrite = 1'b0;
            o_pcwrite = 1'b0;
            o_branch = 1'b0;
            o_pcsrc = 2'b00;
            o_regdst = 1'b0;
            o_memtoreg = 1'b0;
            o_aluop = 2'b00;
            o_alusrca = 1'b0;
            o_alusrcb = 2'b00;
            o_regwrite = 1'b0;
            next_state = FETCH;
        end

        FETCH : begin
            o_iord = 1'b0;
            o_alusrca = 1'b0;
            o_alusrcb = 2'b01;
            o_aluop = 2'b00;
            o_pcsrc = 2'b00;
            o_irwrite = 1'b1;
            o_pcwrite = 1'b1;
            next_state = DECODE;
        end

        DECODE : begin
            o_alusrca = 1'b0;
            o_alusrcb = 2'b11;
            o_aluop = 2'b00;
            if (i_opcode == RTYPE) 
                    next_state = EXECUTE;
            else if(i_opcode == LW || i_opcode == SW) 
                    next_state = MEM_ADR;
            else if(i_opcode == BEQ) 
                    next_state = BRANCH;
            else if(i_opcode == ADDI) 
                    next_state = I_EX;
            else if(i_opcode == JMP) 
                    next_state = JUMP;
            else 
                    next_state = IDLE;
        end

        MEM_ADR : begin
            o_alusrca = 1'b1;
            o_alusrcb = 2'b10;
            o_aluop = 2'b00;
            if(i_opcode == LW)
                next_state = MEM_READ;
            else if(i_opcode == SW)
                next_state = MEM_WRITE;
            else
                next_state = FETCH;
        end

        MEM_READ : begin
            o_iord = 1'b1;
            next_state = MEM_WB;
        end

        MEM_WB : begin
            o_regdst = 1'b0;
            o_memtoreg = 1'b1;
            o_regwrite = 1'b1;
            next_state = FETCH;
        end

        MEM_WRITE : begin
            o_iord = 1'b1;
            o_memwrite = 1'b1;
            next_state = FETCH;
        end

        EXECUTE : begin
            o_alusrca = 1'b1;
            o_alusrcb = 2'b00;
            o_aluop = 2'b10;
            next_state = ALU_WB;
        end

        ALU_WB : begin
            o_regdst = 1'b1;
            o_memtoreg = 1'b0;
            o_regwrite = 1'b1;
            next_state = FETCH;
        end

        BRANCH : begin
            o_alusrca = 1'b1;
            o_alusrcb = 2'b00;
            o_aluop = 2'b01;
            o_pcsrc = 2'b01;
            o_branch = 1'b1;
            next_state = FETCH;
        end

        I_EX : begin
            o_alusrca = 1'b1;
            o_alusrcb = 2'b10;
            o_aluop = 2'b00;
            next_state = I_WB;
        end

        I_WB : begin
            o_regdst = 1'b0;
            o_memtoreg = 1'b0;
            o_regwrite = 1'b1;
            next_state = FETCH;
        end

        JUMP : begin
            next_state = FETCH;
            o_pcsrc = 2'b10;
            o_pcwrite = 1'b1;
        end

        default : begin
            o_iord = 1'b0;
            o_memwrite = 1'b0;
            o_irwrite = 1'b0;
            o_pcwrite = 1'b0;
            o_branch = 1'b0;
            o_pcsrc = 2'b00;
            o_regdst = 1'b0;
            o_memtoreg = 1'b0;
            o_aluop = 2'b00;
            o_alusrca = 1'b0;
            o_alusrcb = 2'b00;
            o_regwrite = 1'b0;
            next_state = IDLE;
        end
    endcase
end


endmodule
