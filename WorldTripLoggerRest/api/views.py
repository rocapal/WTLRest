# -*- coding: utf-8 -*- 
import os
import sys
from subprocess import call
import subprocess

from django.http import HttpResponse, HttpResponseServerError
from django.utils import simplejson
from parser import *
import jsonpickle


JSON_MIMETYPE="application/json"
STATUS_CMD="svstat" 
STATUS_PATH="/home/pi/WTL/WTLCore/scripts/"

def launch_cmd (command):
    code = call (command, shell=True)

def version(request):

    data = {'name': 'WTLRest',
            'version' : '0.1'}

    return HttpResponse(simplejson.dumps(data), JSON_MIMETYPE)


def start (request):

    data = {'code': 200,
            'message': 'WTL started ok!'}
    
    launch_cmd("sudo /etc/init.d/wtl start")
    return HttpResponse(simplejson.dumps(data), JSON_MIMETYPE)


def stop (request):

    data = {'code': 200,
            'message': 'WTL stopped ok!'}

    launch_cmd("sudo /etc/init.d/wtl stop")
    
    return HttpResponse(simplejson.dumps(data), JSON_MIMETYPE)


def status (request):

    proc = subprocess.Popen([STATUS_CMD,STATUS_PATH],stdout=subprocess.PIPE)
    line = proc.stdout.readline()

    code = 1 if line.find("seconds")!=-1 else 0
    msg = ""

    if (code == 1):
        seconds = line.split(" ")[4]
        msg = "WorldTripLogger is running " + seconds + " seconds ago!"
    else:
        msg = "WorldTripLogger is stopped"

    data = {'code': code,
            'message': msg}

    return HttpResponse(simplejson.dumps(data), JSON_MIMETYPE)

    
    
