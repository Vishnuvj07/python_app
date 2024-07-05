import subprocess
status = 'running'
cmd = 'Get-Service | Where-Object {$_.Status -eq "running"} | Select-Object Name | ForEach-Object {$_.Name}'
print(cmd)
services_cmd = subprocess.run(['powershell.exe', cmd], shell= "True", stdout=subprocess.PIPE, stderr= subprocess.PIPE)
print(services_cmd)