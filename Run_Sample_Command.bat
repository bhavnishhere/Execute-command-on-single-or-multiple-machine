delete /Q output_Sample_Command_Execution.txt

REM Here as one host name is given this command will run on one host only. as this argument is passed, so it will get executed on that machine .
REM program wil still loop over all ips but continue if ip/hostname does not match and execute only if it matches.
REM As IP is matched from input csv, if a new hostname or ip is given which is not in input csv all ips will be ignored and command will not et executed on any machine
echo "Removing older folders from HDFS"
python Execute_With_Hostname_support.py input_file_having_ip_And_Hostname.csv "hadoop fs -rm -r -skipTrash /user/ct/somefolder/Daily_BHS_*" username password hostname_orAnyMarkernameforthismachine_1> output_Sample_Command_Execution.txt


REM this command will execute df-kh on all machines provided in input file. here one less argument is passed so the program wil not stop after executing it on one machine.
python Execute_With_Hostname_support.py input_file_having_ip_And_Hostname.csv "df -kh|grep root" root ctadmin > df_Minus_KH_output.txt
df_Minus_KH_output.txt
