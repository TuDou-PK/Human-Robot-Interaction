# http://www.html.it/pag/53419/websocket-server-con-python/
# pip install --user tornado==5.1.1

import sys, os, socket, time, datetime
import importlib, inspect, textwrap
import traceback
import argparse
import random
import modimParameterServer as mps
import dummyrobot
from dummyrobot import *
from write_path import *
from planner import Planner
from drawpath import drawpath

from thread2 import Thread
from threading import Lock

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from say import say

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"



#from interaction_manager import InteractionManager
import interaction_manager

# Global variables

modim_websocket_server = None     # modim websocket handler
run = True                  # main_loop run flag
run_thread = None           # thread running the code
code_running = False        # code running
status = "Idle"             # robot status sent to websocket
last_answer = None          # answer received from web interface (e.g. buttons)
return_value = "OK"         # string to be returned to client
conn_client = None          # Connected client
im = None                   # interaction manager
display_ws = None           # display ws object
robot_type = None           # None, pepper, marrtino, ...
robot_initialized = False   # if robot has been initialized


# Settings functions

def init_interaction_manager():
    global robot_type, robot_initialized, im, display_ws, robot
    print "Start interaction manager"
    print "  -- display init --"
    display_ws = DisplayWS()
    display_ws.cancel_answer()
    display_ws.remove_buttons()
    print "  -- robot init --"
    robot = dummyrobot.DummyRobot()
    if (not robot_initialized): 
        if (robot_type=='pepper'):
            # Connection to robot
            pepper_cmd.robot = pepper_cmd.PepperRobot()
            pepper_cmd.robot.connect()
            if (pepper_cmd.robot.isConnected):
                robot_initialized = True
                robot = pepper_cmd.robot
        elif (robot_type=='marrtino'):
            pass
    im = interaction_manager.InteractionManager(display_ws, robot)


def quit_interaction_manager():
    global robot
    if (robot_type=='pepper'):
        pepper_cmd.robot.quit()


def init_GUI(robot_type,url):
    global robot
    # run in a separate thread (started before wssocket start, so it must wait before connection)
    time.sleep(3)
    if (robot_type=='pepper' and robot!=None and url!=None):
        robot.showurl(url)




def begin():
    # Note: this function is replaced by from <robot>_cmd import *
    print "WS begin"

def end():
    # Note: this function is replaced by from <robot>_cmd import *
    print "WS end"


# Basic UI functions

# Export commands, must set global variable return_value
class DisplayWS:

    def __init__(self):
        self.websocket_server = None
        self.mutex = Lock()
        self.reset_answer = False        # Request to stop waiting for answers

    def setws(self, websocket_server):
        self.websocket_server = websocket_server
    
    def websend(self, data):
        if (self.websocket_server == None):
            print('%sDisplayWS: websocket not connected.%s' %(RED,RESET))
            return
        try:
            self.mutex.acquire()
            self.websocket_server.write_message(data)
            #print(status)
        except:
            # tornado.websocket.WebSocketClosedError:
            print('%sDisplayWS: websocket connection error.%s' %(RED,RESET))
        finally:
            self.mutex.release()

    def display_text(self, data, place):
        global return_value
        cmdsend = "display_text_"+place+"_"+data
        print "web send: " + cmdsend
        self.websend(cmdsend)
        return_value = "OK"

    def display_image(self, data, place='default'):
        global return_value
        cmdsend = "display_image_"+place+"_"+data
        print "web send: " + cmdsend
        self.websend(cmdsend)
        return_value = "OK"

    def display_pdf(self, data, place='default'):
        global return_value
        cmdsend = "display_pdf_"+place+"_"+data
        print "web send: " + cmdsend
        self.websend(cmdsend)
        return_value = "OK"

    def display_imagebuttons(self, data): 
        global last_answer, return_value
        for d in data:
            self.websend("display_imagebutton_"+d+"\n")
            #time.sleep(0.01)
        last_answer = None
        return_value = "OK"

    def display_buttons(self, data): 
        global last_answer, return_value
        self.remove_buttons()
        for d in data:
            print "WebSend: ", "display_button_"+d[0]+"$"+d[1]+"\n"
            self.websend("display_button_"+d[0]+"$"+d[1]+"\n")
            #time.sleep(0.1)
        last_answer = None
        return_value = "OK"

    def remove_buttons(self): 
        global return_value
        self.websend("remove_buttons")
        return_value = "OK"

    def answer(self, timeout=-1):
        global last_answer, return_value
        self.reset_answer = False
        last_answer = None
        answercnt = 0
        answerwait = 0.5
        while (last_answer is None and not self.reset_answer and (timeout<0 or answercnt <= timeout)):
            time.sleep(answerwait)
            answercnt += answerwait
        if timeout>=0 and answercnt > timeout:
            return_value = 'timeout'
        else:
            print("Answer: %s" %last_answer)
            return_value = last_answer
        return return_value

    def setReturnValue(self, rv): # value returned to the client when remote program finishes
        global return_value
        return_value = rv

    def waitfor(self, data):
        while (self.answer()!=data and not self.reset_answer):
            time.sleep(0.5)

    def cancel_answer(self):
        self.reset_answer = True

    def ask(self, data, timeout=30000):
        remove_buttons()
        display_buttons(data)    
        a = answer(timeout)
        remove_buttons()
        if (a is not None):
            a = a.rstrip()
        return a

    def loadUrl(self, data):
        global return_value
        cmdsend = "url_"+data
        print "web send: " + cmdsend
        self.websend(cmdsend)
        time.sleep(3)
        return_value = "OK"


#def sensorvalue(data):
#    global return_value
#    val = None
#    print "Sensor ",data
#    if (data=='headtouch'):
#        val = pepper_cmd.headTouch
#    elif (data=='frontsonar'):
#        val = pepper_cmd.sonarValues[0]
#    elif (data=='backsonar'):
#        val = pepper_cmd.sonarValues[1]
#    print "Sensor value = ",val
#    return val


def client_return():
    global conn_client, return_value, last_answer
    if (conn_client is None):
        return
    try:
        if (last_answer != None):
            conn_client.send("%s\n" %last_answer)
            last_answer = None
        elif (return_value != None):
            conn_client.send("%s\n" %return_value)
            return_value = None
        else:
            conn_client.send("00\n")

    except Exception as e:
        print(RED+"Run code: Connection error"+RESET)
        print e


def ifreset(killthread=False):
    global run_thread, code_running, display_ws
    display_ws.cancel_answer()
    #display_ws.websend("reload")
    time.sleep(0.5)
    client_return()
    if (killthread and code_running):
        try:
            run_thread.terminate()
            print "Run code thread: ",run_thread," terminated."
        except:
            print "Thread already terminated"
        code_running = False


  

# Run the code

def run_code(code):
    global status, return_value, conn_client, im, code_running, last_answer
    if (code is None):
        return

    elif (code[0:2]=='$$'): # name of the folder containing the demo
        fname = code[2:]
        print "Demo ",fname
        code = 's = os.path.join(os.getenv("PEPPER_DEMOS"),"%s") %fname\n'
        code += 'print(s)\n' 
        code += 'im.setDemoPath(s)\n' 

    elif (code[0]=='$'): # python file
        v = str(code[1:]).split('|')
        mname = v[0]
        fct = v[1]
        print("Execute commands in module %s function %s" %(mname,fct))
        mod = importlib.import_module(mname)
        lcode = inspect.getsourcelines(eval('mod.%s' %fct))
        code = ''
        for l in lcode[0][1:]:
            code += l
        code = textwrap.dedent(code)
        code += '\n'
        #code = 'pass'

    print("Executing")
    print(code)

    print("=== Start code run ===")
    try:
        status = "Executing program"
        code_running = True
        exec(code)
        code_running = False
    except SyntaxError as err:
        print("%sCODE SYNTAX ERROR in line %d%s" %(RED,err.lineno,RESET))
        print err
    except Exception as e:
        print("%sCODE EXECUTION ERROR%s" %(RED,RESET))
        cl, exc, tb = sys.exc_info()
        line_number = traceback.extract_tb(tb)[-1][1]
        #print(traceback.extract_tb(tb))
        for l in traceback.extract_tb(tb):
            print("%s:%d" %(l[0],l[1]))
 
        print("%s%s at line %d: %s%s" %(RED,e.__class__.__name__,line_number,e,RESET))

    status = "Idle"
    ifreset()
    print("=== End code run ===")



# TCP command server

def start_cmd_server(TCP_PORT):
    global run, return_value, run_thread, conn_client, code_running

    TCP_IP = ''
    BUFFER_SIZE = 20000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(30000)
    try:
        s.bind((TCP_IP,TCP_PORT))
        s.listen(1)
        run=True
    except:
        print RED+"Cmd Server: bind error"+RESET
        run=False        
    
    while run:

        if (code_running):
            print("%s== Code running: %r ==%s" %(RED,code_running,RESET))
            print("%s== Killing thread !!! ==%s" %(RED,RESET))
            ifreset(True)

        print("%sCmd Server: listening on port %d %s" %(GREEN,TCP_PORT,RESET))

        connected = False
        conn_client = None
        
        while (run and not connected):
            try:
                #print "GUI Waiting for connection ..."
                conn_client, addr = s.accept()
                print "Cmd Connection address:", addr
                connected = True
            except KeyboardInterrupt:
                print "User quit."
                run = False
            except socket.timeout:
                pass
            except Excpetion as e:
                print e
                run = False


        while (run and connected):
            data = ''
            while (run and connected and ((data=='') or (data[0]!='!' and data[0]!='?' and data[0]!='*' and data[0]!='[' and (not '###ooo###' in data)))):
                try:
                    d = conn_client.recv(BUFFER_SIZE)
                except:
                    print "Cmd Server: connection closed."
                    connected = False
                    break
                if (d==''):
                    break
                data = data + d
                #print "Received partial data: ",data

            if (not connected):
                break
            if (data==''):
                break

            #print "Received: ",data

            if (data[0]=='*'):
                print("Control: %s" %data[1:])
                global last_answer
                last_answer = data[1:]
            elif (data[0]=='?'):
                # print('client return...')
                client_return()
            elif (data[0]=='['):
                print("Values: %s" %data)
            elif (data[0]=='!'):
                # parameter message should come in in the form of "! key ! value"
                message=data[1:]
                print("External parameter setting : %s" %message)
                arguments = message.split("!")
                mps.setparam(arguments[0].strip(), arguments[1].strip())             
            else: # python code
                print "Thread start: ",run_thread
                run_thread = Thread(target=run_code, args=(data,))
                run_thread.start()



    #TODO Only if not asked explict load URL        
    ifreset(True)

    if (conn_client is not None):
        conn_client.close()
        conn_client = None
    print "Cmd Server: quit"
        
 



# Modim Websocket server handler

class ModimWebSocketServer(tornado.websocket.WebSocketHandler):

    def open(self):
        global modim_websocket_server, display_ws
        modim_websocket_server = self
        print('New modim websocket connection')
        print modim_websocket_server
        display_ws.setws(modim_websocket_server)
       
    def on_message(self, message):
        global last_answer
        print('Input received:\n%s' % message)
        self.write_message('OK') # reply back to ws client
        # store answer for program client

        def pathfind(goal_str):
            domain = './path1/d1.pddl'
            problem = './path1/p1.pddl'
            planner = Planner()
            plan = planner.solve(domain, problem, goal_str)
            if type(plan) is list:
                path = ''
                paths = []
                paths.extend(plan[0].parameters[1:])

                for act in plan[1:]:
                    paths.append(act.parameters[2])


                paths_pos = ['({}, {})'.format(pos[3], pos[5]) for pos in paths] 
                path = ' -> '.join(paths_pos)
            else:
                print('No plan was found')
                exit(1)
            return path, [(int(pos[3]), int(pos[5])) for pos in paths]

        rooms = {'GYM' : 'sq-1-3', 'WC' : 'sq-1-7', 'Bio' : 'sq-2-7', 
        'A3' : 'sq-2-0', 'A2' : 'sq-2-1', 'A1' : 'sq-2-2', 
        'food': 'sq-2-4', 'B3' : 'sq-2-5', 'B2' : 'sq-2-6', 
        'B1' : 'sq-2-7', 'R1' : 'sq-4-0', 'R2' : 'sq-4-1', 
        'R3' : 'sq-4-2', 'R4' : 'sq-4-3', 'R5' : 'sq-4-4', 
        'R6' : 'sq-4-5', 'R7' : 'sq-4-6', 'R8' : 'sq-4-7' }

        # positions = {'sq-1-3':(0, 3),
        #             'sq-1-7':(0, 7),
        #             'sq-2-2':(1, 2),
        #             'sq-2-3':(1, 3),
        #             'sq-2-4':(1, 1),
        #             'sq-2-5':(1, 1),
        #             'sq-2-6':(1, 1),
        #             'sq-2-7':(1, 1),
        #             'sq-3-8':(1, 1),
        #             'sq-3-9':(1, 1),
        #             'sq-3-10':(1, 1),
        #             'sq-3-1':(1, 1),
        #             'sq-3-1':(1, 1),
        # }

        if message == 'A1':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)

        elif message == 'WC':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)

        elif message == 'A2':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)
            
        elif message == 'A3':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)
            
        elif message == 'door':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)
            
        elif message == 'food':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)
            
        elif message == 'B1':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)
            
        elif message == 'B3':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)
            
        elif message == 'Bio':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)
            
        elif message == 'GYM':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            drawpath(paths)
            say('The path founded: ' + path)
            
        elif message == 'R1':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            say('The path founded: ' + path)
            
        elif message == 'R2':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            say('The path founded: ' + path)
            
        elif message == 'R3':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            say('The path founded: ' + path)
            
        elif message == 'R4':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            say('The path founded: ' + path)
            
        elif message == 'R5':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            say('The path founded: ' + path)
            
        elif message == 'R6':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            say('The path founded: ' + path)
            
        elif message == 'R7':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            say('The path founded: ' + path)
            
        elif message == 'R8':
            path, paths = pathfind(rooms[message])
            write_path(message, 'The path founded: ' + path)
            say('The path founded: ' + path)
            

        last_answer = message
        


    def on_close(self):
        global modim_websocket_server
        print(RED+'Modim Websocket: connection closed'+RESET)
        #TODO Only if not asked explict load URL 
        #ifreset(True)
        modim_websocket_server = None
  
    def on_ping(self, data):
        print('ping received: %s' %(data))
  
    def on_pong(self, data):
        print('pong received: %s' %(data))
  
    def check_origin(self, origin):
        #print("-- Request from %s" %(origin))
        return True

    def sendJS(self, data):
        try:
            self.write_message(data)
            #print(status)
        except:
            # tornado.websocket.WebSocketClosedError:
            print(RED+'Web socket: connection error.'+RESET)



class CtrlWebSocketServer(tornado.websocket.WebSocketHandler):

    def open(self):
        print('New ctrl websocket connection')
       
    def on_message(self, message):
        global last_answer
        print('InCtrl input received:\n%s' % message)
        last_answer = message
  
    def on_close(self):
        print(RED+'Ctrl websocket: connection closed'+RESET)

    def check_origin(self, origin):
        #print("-- Request from %s" %(origin))
        return True


# Code Websocket server handler

class CodeWebSocketServer(tornado.websocket.WebSocketHandler):

    def open(self):
        print('New Code connection')
       
    def on_message(self, message):
        global code, status, robot
        try:
            print('Code received:\n%s' % message)
        except UnicodeEncodeError:
            message = message.encode('utf-8')
        if (message=='stop'):
            print('Stop code and robot')
            robot.stop_request = True
            robot.stop()
        else:            
            if (status=='Idle'):
                t = Thread(target=run_code, args=(message,))
                t.start()
            else:
                print('Program running. This code is discarded.')
        self.write_message('OK')
  
    def on_close(self):
        print('Code Connection closed')
  
    def on_ping(self, data):
        print('ping received: %s' %(data))
  
    def on_pong(self, data):
        print('pong received: %s' %(data))
  
    def check_origin(self, origin):
        #print("-- Request from %s" %(origin))
        return True


# Main program

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-modimwsport", type=str, default=9100,
                        help="MODIM WS Server port.")
    parser.add_argument("-codewsport", type=str, default=9010,
                        help="Code WS Server port.")
    parser.add_argument("-cmdport", type=int, default=9101,
                        help="Command Server port")
    parser.add_argument("-robot", type=str, default=None,
                        help="Robot type [None, pepper, marrtino]")
    parser.add_argument("-url", type=str, default=None,
                        help="URL of main HTML file")

    args = parser.parse_args()

    modim_ws_server_port = args.modimwsport
    code_ws_server_port = args.codewsport
    cmd_server_port = args.cmdport
    robot_type = args.robot

    if (robot_type=='pepper'):
        try:
            pepper_tools_dir = os.getenv("PEPPER_TOOLS_HOME")
            sys.path.append(pepper_tools_dir+'/cmd_server')
            import pepper_cmd
            from pepper_cmd import *
        except Exception as e:
            print e
            print("%sSet environment_variable PEPPER_TOOLS_HOME to pepper_tools directory.%s" %(RED,RESET))
            sys.exit(0)
    elif (robot_type=='marrtino'):
        try:
            marrtino_apps_dir = os.getenv("MARRTINO_APPS_HOME")
            sys.path.append(marrtino_apps_dir+'/program')
            import robot_cmd_ros
            from robot_cmd_ros import *
        except:
            print("%sSet environment_variable MARRTINO_APPS_HOME to marrtino_apps directory.%s" %(RED,RESET))
            sys.exit(0)



    # Run command server
    t = Thread(target=start_cmd_server, args=(cmd_server_port,))
    t.start()

    # Init robot display object and IM
    init_interaction_manager()

    # Run websocket server
    application1 = tornado.web.Application([
        (r'/modimwebsocketserver', ModimWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application1)
    http_server.listen(modim_ws_server_port)
    print("%sModim Websocket server: listening on port %d %s" %(GREEN,modim_ws_server_port,RESET))

    application2 = tornado.web.Application([
        (r'/ctrlwebsocketserver', CtrlWebSocketServer),])  
    ctrl_ws_server_port = modim_ws_server_port + 10
    http_server2 = tornado.httpserver.HTTPServer(application2)
    http_server2.listen(ctrl_ws_server_port)
    print("%sCtrl websocket server: listening on port %d %s" %(GREEN,ctrl_ws_server_port,RESET))

    application3 = tornado.web.Application([
        (r'/websocketserver', CodeWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application3)
    http_server.listen(code_ws_server_port)
    print("%sCode Websocket server: listening on port %d %s" %(GREEN,code_ws_server_port,RESET))


    # Init GUI
    t_initgui = Thread(target=init_GUI, args=(robot_type, args.url,))
    t_initgui.start()

    # Start websocket server
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print(" -- Keyboard interrupt --")
    try:
        modim_websocket_server.close()
    except:
        pass

    print("Web server quit.")
    run = False

    quit_interaction_manager()

    print("Waiting for main loop to quit...")

    sys.exit(0)

