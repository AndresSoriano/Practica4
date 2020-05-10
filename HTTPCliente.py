import argparse
import http.client
import urllib.parse
#REMOTE_SERVER_HOST = 'www.python.org'
REMOTE_SERVER_PATH = '/'
'''www.python.org'''

def metodos(opc):
    conn = http.client.HTTPConnection('localhost', 8080)
    #conn = http.client.HTTPConnection(REMOTE_SERVER_HOST)
    if opc == 1:
        conn.request("GET", "/")
        r1 = conn.getresponse()
        print("Codigo y Razón")
        print(r1.status, r1.reason)
        data1 = r1.read()
        conn.request("GET", "/")
        r1 = conn.getresponse()
        print("Cuerpo de la respuesta")
        while True:
            chunk = r1.read(200)
            if not chunk:
                break
            print(repr(chunk))
    else:
        if opc == 2:
            conn.request("HEAD", "/")
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            data1 = r1.read()
            print(data1 == b'')
        else:
            if opc == 3:
                params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn.request("POST", "", params, headers)
                r1 = conn.getresponse()
                print(r1.status, r1.reason)
                data1 = r1.read()
                print(data1)
                conn.close()
            else:
                if opc == 4:
                    conn.request("PUT", "new.html")
                    r1 = conn.getresponse()
                    print("Codigo y Razon")
                    print(r1.status, r1.reason)
                else:
                    if opc == 5:
                        conn.request("DELETE", "new.html")

                        r1 = conn.getresponse()
                        print("Codigo y Razon")
                        print(r1.status, r1.reason)

ciclo = -1
while ciclo != 0:
    print("METODOS\n1=GET\n2=HEAD\n3=POST\n4=PUT\n5=DELETE\n")
    ciclo = int(input())
    metodos(ciclo)
