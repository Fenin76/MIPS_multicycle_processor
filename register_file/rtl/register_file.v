`timescale 1ns / 1 ps

module register_file(i_clk,
                     i_a1,  //address 1
                     i_a2,  //address 2
                     i_a3,  //address 3 /data
                     i_wd3, //write data3 32 bit
                     i_we3, //enable write of reg
                     o_rd1, //read data 1
                     o_rd2  //read data 2
                    );

input i_clk;
input [4:0] i_a1; //to address 32x32bit register (5 bits = 32)
input [4:0] i_a2;
input [4:0] i_a3;
input [31:0] i_wd3; //write data input for 32 bit reg
input i_we3;

output wire [31:0] o_rd1; //output wrte data1
output wire [31:0] o_rd2; //output wite data2


reg [31:0] internal_reg_file [31:0]; //32 x 32 bit registers for storage of instruction/data

always @ (posedge i_clk) begin

    if(i_we3 == 1'b1) begin
        internal_reg_file[i_a3] <= i_wd3;
    end
end

assign o_rd1 = internal_reg_file[i_a1];
assign o_rd2 = internal_reg_file[i_a2];

endmodule
