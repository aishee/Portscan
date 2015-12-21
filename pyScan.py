#!/usr/bin/python

import optparse
from threading import *
from socket import *
screenLock = Semaphore(value=1)


def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('Scan Port\r\n')
        result = connSkt.recv(100)
        screenLock.acquire()
        print('[+]%d/tcp open '%tgtPort)
        print('[+] '+str(result))
    except:
        screenLock.acquire()
        print('[-]%d/tcp closed'%tgtPort)
    finally:
        screenLock.release()
        connSkt.close()

def portScan(tgtHost, tgtPort):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host"%tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print("\n[+] Scan result for: "+tgtName[0])
    except:
        print('Scan result for: ' + tgtIP)
    setdefaulttimeout(1)
    for tgtPorts in tgtPort:
        t=Thread(target=connScan, args=(tgtHost, int(tgtPorts)))
        t.start()
def main():
    parser = optparse.OptionParser('usage %prog -H ' + '<target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] inside\"\" separated by commas')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPort =  str(options.tgtPort).split(", ")
    if(tgtHost==None) | (tgtPort[0]==None):
        print(parser.usage)
        exit(0)
    portScan(tgtHost, tgtPort)
if __name__ == "__main__":
    main()
