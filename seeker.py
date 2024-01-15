import pyfiglet
import re
import socket
import argparse
import json
import os
from colorama import init,Fore
from threading import Thread,Lock
from queue import Queue
from prettytable import PrettyTable



#Global declarations

init()
GREEN=Fore.GREEN
RESET=Fore.RESET
GRAY=Fore.LIGHTBLACK_EX
RED=Fore.RED
line=Queue()
print_lock=Lock()
host_pattern=r"[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}"
out=pyfiglet.figlet_format("SEEKER",font="rectangles")
service_bool=False
out_bool=False
open_port=[]
pretty=PrettyTable()
pretty.field_names=["Port no.","Protocol","State","Service"]

#Class definition

class Seeker:
  
    def __init__(self,host,ports,service_bool,out_bool,time_out=1.0) -> None:
        self.host=host
        self.ports=ports
        self.service_bool=service_bool
        self.out_bool=out_bool
        self.num_thread=200 
        self.time_out = time_out


    def start_scan(self):
        while True:
            worker= line.get()
            self.port_scan(worker)
            line.task_done()
            
        
    def port_scan(self,port):
        
        s = socket.socket(socket.AF_INET)
        s.settimeout(self.time_out)
        result=s.connect_ex((host, port))
        if result==0:
            if self.service_bool:
                str_port=str(port) 
                self.service_print(str_port)  
            else:
                with print_lock:
                    print(f"{GREEN}{self.host:15}:{port:5} is open{RESET}")
                    if self.out_bool:
                        with open(f"{args.output}/seek_{self.host}.txt","a") as out_obj:
                            out_obj.write(f"{self.host:15}:{port:5} is open.\n")

        
        s.close()
  
    def threader(self):
        for t in range(self.num_thread):
            t=Thread(target=self.start_scan)
            t.daemon=True
            t.start()
        for worker in self.ports:
            line.put(worker)
        line.join()      
        if service_bool:
            print(pretty)
            
        print("Scan Complete!") 
        
    def service_print(self,p):   
        tcp=data[p][0]["tcp"]
        udp=data[p][0]["udp"]
        service=data[p][0]["description"]
        if tcp and udp:
            protocol="tcp/udp"
        else:
            protocol="tcp" if tcp else "udp"
        open_port.append(GREEN+str(p)+RESET)
        open_port.append(protocol)
        open_port.append(GREEN+"open"+RESET)
        open_port.append(service)       
        pretty.add_row(open_port)        
        open_port.clear()
        if self.out_bool:
            self.out_file_op(p,service,protocol)

    def out_file_op(self,port_num,svc,proto):
        with open(f"{args.output}/seek_{self.host}.txt","a") as out_obj:
                            out_obj.write(f"Port number: {port_num}\n")
                            out_obj.write(f"Protocol: {proto}\n")
                            out_obj.write(f"State: open\n")
                            out_obj.write(f"Service: {svc}\n\n")


        
# Parser declartions and initializations

parser =argparse.ArgumentParser(description="Seeker 1.1",usage="seeker.py <IPv4 address> [Scan type flags]")
parser._print_message(RED+out+RESET)
parser.add_argument("host",help="IPv4 of the host to scan.\n")
parser.add_argument("-p","--ports",help="Scan a specific port,\n use \"-\" to specify a port range.")
parser.add_argument("-q","--quick",action="store_true",help="Quick scan the top 100 ports.")
parser.add_argument("-a","--all",action="store_true",help="Scan all ports (0-65535).")
parser.add_argument("-sV","--service",action="store_true",help="Display port services.")
parser.add_argument("-o","--output",type=str,help="Store the output in a text file at the path .")
parser.add_argument("-st","--set_timeout",type=float,help="Set timeout for response.")
args=parser.parse_args()

# Argument processing 

host= args.host
if not re.match(host_pattern,host):
    print("Incorrect host address. Enter the correct IP address!")
    exit(0)

if args.service:
    service_bool=True
    j_obj=open("port_service.json")
    data=json.load(j_obj)
time_out = 1.0
if args.set_timeout:
    time_out = args.set_timeout

if args.output:
    if os.path.exists(args.output):
        out_bool=True
        with open(f"{args.output}/seek_{host}.txt","w") as out_obj:
             out_obj.write(out)      
                           
    else:
        print("Path does not exist!") 

if args.ports:
    if  args.ports.find("-")== -1:
        final_port=[int(args.ports)]
    else:
        port_range=args.ports.split("-")
        start_port,end_port=int(port_range[0]),int(port_range[1])
        final_port=[p for p in range(start_port,end_port+1)]

elif args.quick:
    with  open("quick_ports.txt","r")  as f:
        port_list=f.readlines()
        final_port=[int(p) for p in port_list]

elif args.all:
    final_port=[p for p in range(1,65536)]

else:
    with  open("default_ports.txt","r")  as txt_obj:
        port_list=txt_obj.readlines()
        final_port=[int(p) for p in port_list]

# Seeker class object

obj=Seeker(host,final_port,service_bool,out_bool,time_out=time_out)
obj.threader()
