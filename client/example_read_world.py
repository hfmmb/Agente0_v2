import client
import ast
import random

class Client:
    def __init__(self,HOST='127.0.0.1',PORT=50000):
        self.host = HOST
        self.port = PORT
    def print_message(self,data):
        print("Data:",data)
    def connect(self):
#        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))
#            return(0)
#        except:
#            print('A connection error occurred!')
#            return(-1)
    def execute(self,action,value,sleep_t = 0.5):
        self.s.sendall(str.encode(action+" "+value))
        data = self.s.recv(2048)
        print('Received', repr(data))
        msg = data.decode()
        #message(ast.literal_eval(data.decode()))
        time.sleep(sleep_t)
        return msg






def getMaxCoord():        
	msg = c.execute("info","maxcoord")
	max_coord =ast.literal_eval(msg)
	# test
	print('Received maxcoord', max_coord)
	return max_coord   

def getObstacles():
	msg = c.execute("info","obstacles")
	w_map =ast.literal_eval(msg)
	# test
	print('Received map:', w_map)
	return w_map

def main():
	res = getMaxCoord()
	print("Max coord x:",res[0])
	print("Max coord y:",res[1])
	# Get information of the world		
	# Print the obstacles position
	obstacles = getObstacles()
	print("Obstacles 0 1 =", obstacles[0][1])	
	# Print the position
	#Print a list of possible positions from the actual position 
		
	# Test if any position in the list is a goal
	# For each element in the list, expand it for the next possible positions (don't include position already in the previous list)
	# Test if any position in the list is a goal
	# Etc

#STARTING PROGRAM
print("Starting client!")
c = client.Client('127.0.0.1', 50000)
res = c.connect()
random.seed() #To become true random, a different seed is used! (clock time)
if res!=-1:
	main()


