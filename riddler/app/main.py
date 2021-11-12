from fastapi import FastAPI, HTTPException
import requests
import subprocess
import sys
app = FastAPI()

API_URL = "https://c8d0349b32a03c4882ed3168a992809d.balena-devices.com/answer"

class Commander:
    def __init__(self):
        self.__user_msg = None
        self.__stop_cmd = None

    @property
    def user_message(self):
        return self.__user_msg

    @property
    def command(self):
        return None
    
    @command.setter
    def command(self, value):
        self.__data = value
    
    def run(self):
        cmd = ''
        should_stop_last_cmd = self.__stop_cmd != None
        if should_stop_last_cmd:
            cmd = f'{self.__stop_cmd}; '
        self.__user_msg = self.__data.get('msg')
        self.__stop_cmd = self.__data.get('stop')
        cmd += self.__data['start']
        subprocess.Popen(cmd, stdout=sys.stdout, shell=True)

cmdr = Commander()

@app.get("/answer/{code}")
def read_item(code: str):
    puzzle_package = requests.get(f"{API_URL}/{code}")
    if puzzle_package.status_code != 200:
        raise HTTPException(status_code=404, detail="So close!")
    # example puzzle package:
    # {
    #     "start": "docker run --name puzzz --privileged builder555/expired-glucose",
    #     "stop": "docker container stop puzzz; docker rm puzzz",
    #     "msg": "Hahaha! You are right, there are only 14. I Lied!",
    # }
    data = puzzle_package.json()
    cmdr.command = data
    cmdr.run()
    return {'msg': cmdr.user_message or 'Well done!'}
