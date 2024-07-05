from fastapi import FastAPI, responses as rp, Request, Body, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import json
import secrets
import os
import subprocess

app = FastAPI()

@app.post('/login/')
def get_login(info:Request,id: str= Body(), password: str= Body()):
    token = secrets.token_urlsafe(16) #22bit
    print(token)
    cont = {"status" : "Success", "user_id": id, "user_token": token}
    return json.dumps(cont)

@app.get('/hosts/hostname')
def read_host():
    my_host = os.environ['COMPUTERNAME']
    print(my_host)
    rt = '''<?xml version="1.0"?>
    <sample>
    <Header>
        HOSTNAME :
    </Header>
    <Body>
        ''' +my_host+ '''
    </Body>
    </sample>'''
    return rp.Response(content = rt, media_type="application/xml")

@app.get("/host/{file_type}")
async def get_py_file(file_type: str):
    path = ""
    items = os.listdir(path)
    files = [item for item in items if item.endswith(file_type)]
    #return {"files": files}
    return rp.JSONResponse(content= {"files": files}, status_code= 200, media_type= "application/json")

@app.get("/services/{status}")
async def get_service_status(status: str):
    if status in('running, stopped'):
        cmd = 'Get-Service | Where-Object {$_.Status -eq "'+status+'"} | Select-Object Name | ForEach-Object {$_.Name}'
        services_cmd = subprocess.run(['powershell.exe', cmd], shell= "True", stdout=subprocess.PIPE, stderr= subprocess.PIPE)
        print(services_cmd.stdout.decode('utf-8'))
        services = [ser.strip() for ser in services_cmd.stdout.splitlines()]
        return {status : services}
    else:
        raise HTTPException(status_code=404, detail= "invalid status input")
    
# main driver function
if __name__ == '__main__':
    uvicorn.run(app)