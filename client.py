import socket, select, string, sys
import json

def display() :
	you="\33[33m\33[1m"+" You: "+"\33[0m"
	sys.stdout.write(you)
	sys.stdout.flush()

def send_json (sock, message):
	sock.send(bytes(json.dumps(message)))

def main():

    if len(sys.argv)<2:
        host = raw_input("Enter host ip address: ")
    else:
        host = sys.argv[1]

    port = 5001

    name=raw_input("\33[34m\33[1m CREATING NEW ID:\n Enter username: \33[0m")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try :
        s.connect((host, port))
    except :
        print "\33[31m\33[1m Can't connect to the server \33[0m"
        sys.exit()

    send_json(s, name)
    display()
    while 1:
        socket_list = [sys.stdin, s]

        rList, wList, error_list = select.select(socket_list , [], [])

        for sock in rList:
            #incoming message from server
            if sock == s:
                jsonData = sock.recv(4096)
                try:
                    data = json.loads(jsonData)
                except ValueError as e:
                    print '\33[31m\33[1m \rDISCONNECTED!!\n \33[0m'
                    sys.exit()

                if not data :
                    print '\33[31m\33[1m \rDISCONNECTED!!\n \33[0m'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    display()

            #user entered a message
            else :
                msg=sys.stdin.readline()
                send_json(s, msg)
                display()

if __name__ == "__main__":
    main()
