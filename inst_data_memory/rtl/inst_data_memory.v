`timescale 1ns / 1ps

module inst_data_memory(i_clk,
                        i_addr,
                        i_we, 
                        i_wdata,
                        o_rdata);

input i_clk;
input i_we;
input [31:0] i_addr;
input [31:0] i_wdata;

output wire [31:0] o_rdata;

parameter depth_inst = 256;
parameter depth_data = 256;

wire [8:0] masked_addr;
reg [31:0] inst_mem [depth_inst-1:0];
reg [31:0] data_mem [depth_data-1:0];

assign masked_addr = i_addr[8:0];

always @ (posedge i_clk) begin
    if (i_we) begin
         if (masked_addr[8] == 1'b1) 
                data_mem[masked_addr[7:0]] <= i_wdata;
         else  
                inst_mem[masked_addr[7:0]] <= i_wdata;
    end

end

assign o_rdata =  (masked_addr[8]==1'b1) ? data_mem[masked_addr[7:0]] : inst_mem[masked_addr[7:0]];

endmodule

