# -*- coding: utf-8 -*- 
import os
import sys
from subprocess import call
import subprocess

from django.http import HttpResponse, HttpResponseServerError
from django.utils import simplejson
from django.core.servers.basehttp import FileWrapper
from parser import *
import jsonpickle


JSON_MIMETYPE="application/json"
STATUS_CMD="svstat" 
STATUS_PATH="/home/pi/WTL/WTLCore/scripts/"
TRACES_PATH="/home/pi/WTLv2-data/"

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


    proc = subprocess.Popen(["du", "-sh","/home/pi/WTLv2-data/"],stdout=subprocess.PIPE)
    line = proc.stdout.readline()
    size = line.split("\t")[0]


    proc = subprocess.Popen(["df", "-h"],stdout=subprocess.PIPE)
    line = proc.stdout.readline()
    line = proc.stdout.readline()
    free_size = line.split(" ")[14]
    porcent_free_size =line.split(" ")[16]

    data = {'code': code,
            'message': msg,
            'size': size,
            'free_size': free_size,
            'porcent_free_size': porcent_free_size }

    return HttpResponse(simplejson.dumps(data), JSON_MIMETYPE)

    
def traces_list (request):

    files = os.listdir(TRACES_PATH)
    ltraces = []
    for trace in files:
        if (trace[len(trace)-1] == 'D'):
            ltraces.append(trace[:len(trace)-1])
        
        
    ltraces = sorted(ltraces,reverse=True)
    data = {'code': 1,
            'traces': ltraces[0:20] }

    return HttpResponse(simplejson.dumps(data), JSON_MIMETYPE)


def trace_data (request, trace):


    try:
        data_file = open(TRACES_PATH + trace + "D")
        lines = data_file.readlines()
    
        data = {'code': 1,
                'datetime' : lines[0].strip(),
                'latitude' : lines[1].strip(),
                'longitude': lines[2].strip(),
                'altitude' : lines[3].strip(),
                'speed'    : lines[4].strip(),
                'temp'     : lines[5].strip(),
                'image'    : trace}

        return HttpResponse(simplejson.dumps(data), JSON_MIMETYPE)

    except IOError:
        
        data = {'code'   : 0,
                'message': trace + " file doesn't exist" }

        return HttpResponseServerError(simplejson.dumps(data), JSON_MIMETYPE)


def trace_image (request, trace):

    try:
        image_path = TRACES_PATH + trace + "I"
        image_file = open (image_path)
        response = HttpResponse(FileWrapper(image_file), content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename=' + trace + '.jpg'
        return response

    except IOError:

        data = {'code'   : 0,
                'message': trace + " file doesn't exist" }

        return HttpResponseServerError(simplejson.dumps(data), JSON_MIMETYPE)
