
import SimpleHTTPServer
import SocketServer
import logging
import cgi
import serial
import sys
import json
import signal

PORT = 3000
planted = False

#If we ctrl+C out of python, make sure we close the serial port first
#handler catches and closes it
def signal_handler(signal, frame):
    ser.close()
    sys.exit(0)



class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


    #SimpleHTTPServer doesn't handle post by default. Hacked up way to do it here
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        jsonString = str(self.rfile.read(length))
        print jsonString
        print "---"
        jsonDict = json.loads(jsonString)
        #From here we have a JSON dict, that has whatever data CS is sending

        #For the timer, all we care about is the the 'round' key 

        if 'round' in jsonDict:
            rounds = jsonDict['round']
            if 'bomb' in rounds:
                #If bomb has been planted, then send the 'P' message
                if rounds['bomb'] == "planted":
                    planted = True
                    print "Bomb has been planted"
                    ser.write('P')
                #If bomb has been defused, then send the 'C' message
                if rounds['bomb'] == "defused":
                    planted = False
                    ser.write('C')
                    print "bomb has been defused"

            #if the round ends, either bomb exploded or everyone died. 
            #Send the 'C' message to stop timer.
            if 'previously' in jsonDict:
                if 'round' in jsonDict['previously']:
                    if 'bomb' in jsonDict['previously']['round']:
                        planted = False
                        print "Round ran out"
                        ser.write('C')
                
        #not sure if a response is really required. Send it anyway
        response = bytes("This is the response.") #create response

        self.send_response(200) #create header
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response) #send response


Handler = ServerHandler
#On windows, Serial ports are usually COM1-3
#On mac/linux this will be different
ser = serial.Serial('COM3')
#Set up our handler for ctrl+c
signal.signal(signal.SIGINT, signal_handler)

#Start server
httpd = SocketServer.TCPServer(("", PORT), Handler)


#Run server
httpd.serve_forever()
