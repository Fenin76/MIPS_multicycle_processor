`timescale 1ns / 1ps

module dff_en(i_clk,
              i_en,
              i_reset,
              i_data,
              o_data);


input i_clk;
input i_reset;
input i_en;
input [31:0] i_data;

output reg [31:0] o_data;

always @ (posedge i_clk)begin
    if (i_reset == 1'b1) begin
        o_data <= 32'b0;
    end else begin
        if (i_en == 1'b1)  
            o_data <= i_data;
    end
end

endmodule