import paramiko
import sys
import re
import csv

if len(sys.argv) < 5 or len(sys.argv) > 6:
    print(f"Usage: {sys.argv[0]} <file-with-IPs> <command-to-execute> <username> <password> [optional: hostname or IP]")
    print(f"Handled one command for formatted result which is 'df -kh|grep root'")
    print(f"2 Sample example commands with only IP given in the input file:")
    print(f"python {sys.argv[0]} IPR_ip_list.txt \"df -kh|grep root\" root ctadmin")
    print(f"python {sys.argv[0]} IPR_ip_list.txt \"df -kh\" root ctadmin")
    print(f"2 Sample example commands with only IP and hostname given in the input file:")
    print(f"python {sys.argv[0]} IPR_ip_list.csv \"df -kh|grep root\" root ctadmin")
    print(f"python {sys.argv[0]} IPR_ip_list.csv \"df -kh\" root ctadmin")
    print(f"To execute the command on a specific server, provide either the hostname or IP as an additional argument.")
    sys.exit(1)

filename = sys.argv[1]
command_To_Execute = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
target_server = sys.argv[5] if len(sys.argv) == 6 else None

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with open(filename, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        ip = row[0].strip()
        hostname = row[1].strip() if len(row) > 1 else ""
        
        if target_server and target_server != ip and target_server != hostname:
            continue
        
        print(f"\n{command_To_Execute} on {ip} ({hostname}):")
        try:
            ssh.connect(ip, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command_To_Execute)
            output = stdout.read().decode()
            if command_To_Execute == 'df -kh|grep root':
                output = re.sub(r'\s+', ' ', output)
                parts = output.split(' ')
                Size = parts[-6]
                Used = parts[-5]
                Avail = parts[-4]
                use_percent = parts[-3]
                print(f"Size={Size} Used={Used}, Avail={Avail}, use_percent={use_percent}")
            else:
                print(output)
        except Exception as e:
            print(f"Error running {command_To_Execute} on {ip} ({hostname})")
            print(str(e))
        finally:
            ssh.close()
