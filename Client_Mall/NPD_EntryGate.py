import cv2
import numpy as np
import easyocr
import time
import mysql.connector as sql
import time
import DatabaseInitializer as dbi
from web3 import Web3
def most_frequent(List):
    return max(set(List) , key = List.count)

#parking spaces
Parking_Spaces = [1,2,3,4,5,6,7,8,9]
#Blockchain provider
provider = Web3.HTTPProvider('https://liberty20.shardeum.org/')
w3 = Web3(provider)

contract_address = Web3.toChecksumAddress("0xb7a03b6c1531f89dc31b7A37bE4A7D3685e8734b")
contract_abi =  [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "businessID",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "addBalanceToBusiness",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "userID",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "addBalanceToUser",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "businessID",
          "type": "uint256"
        }
      ],
      "name": "addBusiness",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "userID",
          "type": "string"
        }
      ],
      "name": "addUser",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "businesses",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "businessID",
          "type": "uint256"
        }
      ],
      "name": "getBusinessBalance",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "userID",
          "type": "string"
        }
      ],
      "name": "getUserBalance",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getUserIDs",
      "outputs": [
        {
          "internalType": "string[]",
          "name": "",
          "type": "string[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "businessID",
          "type": "uint256"
        }
      ],
      "name": "resetBusinessBalance",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "userID",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "businessID",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "transferBalanceFromUserToBusiness",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "userCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "userlist",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "name": "users",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]



contract = w3.eth.contract(address=contract_address, abi=contract_abi)

sender_address = Web3.toChecksumAddress("0x509DdF2bd836Aff26790a51B33A6fE33bE587674")
w3.eth.defaultAccount = sender_address
result = contract.functions.getUserIDs().call()

# Load the cascade for detecting number plates
plate_cascade = cv2.CascadeClassifier('.\haarcascade_plate_number.xml')

#get database password
with open("./dbp.txt",'r') as dbpf:
    pw = dbpf.read()
    dbpf.close()

#Database Connector Object
try:
    conn=sql.connect(host='localhost',user='root',passwd=pw,database='mallDatabase',charset='utf8')
    cur = conn.cursor()
except:
    dbi.create_database(pw)
    time.sleep(4)
    conn=sql.connect(host='localhost',user='root',passwd=pw,database='mallDatabase',charset='utf8')
    cur = conn.cursor()

TakenPS = []
"""
try:
    cur.execute("select Pspace from data")
    TakenPS = cur.fetchall()
    print(TakenPS)

except Exception as e:
    print(e)"""

# Start the webcam
cap = cv2.VideoCapture(0)

# Load the EasyOCR model
reader = easyocr.Reader(['en'])
nlist = []

while True:
    # Read each frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect number plates in the frame
    plates = plate_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw a rectangle and display the number for each detected number plate
    for (x, y, w, h) in plates:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Use EasyOCR to extract the number from the roi
        text = reader.readtext(roi_gray)

        if text:
            text = text[0][1]
            nlist.append(text)
        else:
            text = ""

        # Draw a rectangle around the number plate and display the number
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        if(len(nlist)>20):
            uid = most_frequent(nlist)
            print(uid)
            now = int(time.time())
            print(now)
            nlist.clear()
            uid = uid.replace(" ","")
            uid = uid.lower()
            if uid in result:
                try:
                    st = "INSERT INTO data(user_id,time) values('{}','{}')".format(uid,now)
                    cur.execute(st)
                    conn.commit()
                    print("User registered, open the gate.")
                except:
                    print("Failed To Add Data to database! Please Try Again")
            else:
                print("User not found")
            result = contract.functions.getUserIDs().call()
            time.sleep(10)
            
    # Display the resulting frame
    cv2.imshow('Number Plate Detection', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()

