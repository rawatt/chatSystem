from helper import  *
import socket
import signal
def runClient(serverip,serverport,caip,caport):
    signal.signal(signal.SIGINT, signal_handler)

    print("client connecting to",serverip,serverport,caip,caport)

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client:
        client.connect((serverip, serverport))

        publicKeyServer=getPublicKeyFromCA(caip,caport,serverport)
        # hardcoded value for testing
        id = 8080 if serverport == 9090 else 9090
        privateKeyLocal=getPrivateKey(id)
        while True:#run in a infinite loop and take input until user press ctrl c
            # take input
            data=input()
            if(len(data)<=245):
                # encrypt the input then send it in the form of bytes
                encryptedData=encrypt(publicKeyServer,data)
                client.sendall(encryptedData)

                #receive the acknowledgement from the server, decrypt it and then decode it from the byte form
                data=client.recv(2048)
                decrypted_data=decrypt(privateKeyLocal,data)
                print(decrypted_data)
            else :
                print("max input size is 245 bytes")

    return 0

if __name__=="__main__":
    runClient('127.0.0.1',8080,"127.0.0.1",8081)