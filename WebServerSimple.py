import serial
import re
import time
import threading
import json
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

dataflow = {'Time': '', 'Flow1': 0, 'Flow2': 0, 'Flow3': 0, 'Flow4': 0}          

class SerialThread (threading.Thread):
    def run (self):
        global dataflow                

        # flowmeter parameters
        flow1_ppl = 450.        # pulses per liter
        flow2_ppl = 450.        # pulses per liter
        flow3_ppl = 450.        # pulses per liter
        flow4_ppl = 450.        # pulses per liter

        serialport = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)
    
        while True:
            response = serialport.readlines(None)

            try:
                matchObj = re.match(r'(.*)-(.*)-(.*)-(.*)-(.*)', response[0])
            except:
                matchObj=False
        
            if matchObj:
                timestr = time.strftime("%H:%M:%S %d-%m-%Y")
                flow1 = int(matchObj.group(2),16)
                flow2 = int(matchObj.group(3),16)
                flow3 = int(matchObj.group(4),16)
                flow4 = int(matchObj.group(5),16)
                flow1lpm = (flow1/flow1_ppl*30.)
                flow2lpm = (flow2/flow2_ppl*30.)        
                flow3lpm = (flow3/flow3_ppl*30.)
                flow4lpm = (flow4/flow4_ppl*30.)        
                print timestr,"\tFlow 1:",'%.2f' % flow1lpm,"l/min\tFlow 2:",'%.2f' % flow2lpm,"l/min\tFlow 3:",'%.2f' % flow3lpm,"l/min\tFlow 4:",'%.2f' % flow4lpm,"l/min"
                dataflow['Time']  = timestr
                dataflow['Flow1'] = round(flow1lpm, 2)
                dataflow['Flow2'] = round(flow2lpm, 2)
                dataflow['Flow3'] = round(flow3lpm, 2)
                dataflow['Flow4'] = round(flow4lpm, 2)
            
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        global dataflow


        if self.path=="/flow.json":
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(dataflow))
        else:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Flowmeter</title>\n</head>\n<body>\n<h1>Flowmeter</h1>\n")
            self.wfile.write("<p>Time: %s</p>\n" % dataflow['Time'])
            self.wfile.write("<p>Flow1: %0.2f l/m</p>\n" % dataflow['Flow1'])
            self.wfile.write("<p>Flow2: %0.2f l/m</p>\n" % dataflow['Flow2'])
            self.wfile.write("<p>Flow3: %0.2f l/m</p>\n" % dataflow['Flow3'])
            self.wfile.write("<p>Flow4: %0.2f l/m</p>\n" % dataflow['Flow4'])
            self.wfile.write("</body>\n</html>\n")
        return

    #Handler for the GET requests
    def do_POST(self):
        print self.path
        return
        
class HTTPThread (threading.Thread):
    def run (self):
        PORT_NUMBER = 8080

        try:
            #Create a web server and define the handler to manage the
            #incoming request
            server = HTTPServer(('', PORT_NUMBER), myHandler)
            print 'Started httpserver on port ' , PORT_NUMBER
    
            #Wait forever for incoming htto requests
            server.serve_forever()

        except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            server.socket.close()
    

print "press Ctrl-C to finish"
f = SerialThread()
f.daemon = True
f.start()
s = HTTPThread()
s.daemon = True
s.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print ""
    print "goodbye"