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

#BUSINESS ID
Business_ID = 18002086633

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
nonce = w3.eth.getTransactionCount(sender_address)

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

            cur.execute("select * from data")
            Car_data = cur.fetchall()
            count = cur.rowcount
            found = 0
            duration = 0
            charge = 0

            for i in Car_data:
               if uid == i[0]:
                  duration = now - int(i[1]);
                  duration = duration//3600
                  charge = 40 + duration * 10
                  # uid, Business_ID, charge
                  try: 
                     transaction = contract.functions.transferBalanceFromUserToBusiness(uid,Business_ID,charge).buildTransaction({
                         'gas': 2000000,
                         'gasPrice': w3.toWei('50', 'gwei'),
                         'nonce': w3.eth.getTransactionCount(sender_address),
                     })

                     # Sign and send the transaction
                     signed_txn = w3.eth.account.signTransaction(transaction, private_key='1bc9616d0c1916ae1f32d0af29e88fb41eb01db2a16371bbe821f752b3d21d7a')
                     tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

                     print(tx_hash)
                     print("Transaction Completed Successfully.")
                     found = 1
                  except Exception as e:
                     print("Transaction Failed!",e)
                  
            if found:
               print(f"Vehicle No. {uid} , charge : {charge}, vahicles left : {count-1}")
               st2 = f"delete from data where user_id = '{uid}'"
               cur.execute(st2)
               conn.commit()
               time.sleep(10)
            else:
               print("error, please try again")
               time.sleep(4)
            
    # Display the resulting frame
    cv2.imshow('Number Plate Detection', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()

