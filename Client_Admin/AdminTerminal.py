from web3 import Web3
import mysql.connector as sql
import time
import DatabaseInitializer as dbi

#get database password
with open("./dbp.txt",'r') as dbpf:
    pw = dbpf.read()
    dbpf.close()

#Database Connector Object
try:
    conn=sql.connect(host='localhost',user='root',passwd=pw,database='MallEZ_Admin_Database',charset='utf8')
    cur = conn.cursor()
except:
    dbi.create_database(pw)
    time.sleep(4)
    conn=sql.connect(host='localhost',user='root',passwd=pw,database='MallEZ_Admin_Database',charset='utf8')
    cur = conn.cursor()

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

# Establish a connection to the Ethereum network and unlock the account
w3.eth.defaultAccount = sender_address

# Get the nonce for the sender's account
nonce = w3.eth.getTransactionCount(sender_address)

# Define the data to be sent in the transaction
data = contract.functions.getUserIDs().buildTransaction({
    'gas': 100000,
    'gasPrice': w3.toWei('20', 'gwei'),
    'nonce': nonce,
})

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(data, private_key='1bc9616d0c1916ae1f32d0af29e88fb41eb01db2a16371bbe821f752b3d21d7a')

# Broadcast the transaction
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

   


print(" ===================== MallEZ Admin Terminal ========================")
while True:
   print("Available Commands:")
   print("1 => getUserIDs() : requires no input, returns list of registered users stored in contract")
   print("2 => getBusinessBalance(business_id) : requires input (Business ID of mall) , returns balance aquired by the mall")
   print("3 => resetBusinessBalance(business_id) :  requires input (Business ID of mall),  resets the balance of business back to zero")
   print("4 => addUser(userID) : requires user_id numberplate, adds user to the system with 0 initial balance.")
   print("5 => addBalanceToUser(userID, amount) : requires user_id numberplate & amount to be added , adds balance to users wallet. ADMIN ONLY")
   print("6 => addBusiness(businessID) : requires business_number, Adds business to the system. ADMIN ONLY.")
   print("7 => addBalanceToBusiness(businessID, amount) : requires business_id and amount to be added, adds balance to businesse's wallet. ADMIN ONLY")
   print("8 => transferBalanceFromUserToBusiness(userID, businessID, amount) : requires userID, businessID,& amount to be transfered. Transfers balance from user's wallet to businesse's wallet. ADMIN ONLY")
   print("9 => Get Registered Businesses : Stored in local database, corresponds to business id on blockchain ")
   x = int(input("Enter your choice (integer 1-8) : "))
   if (x == 1):
      result = contract.functions.getUserIDs().call()
      print(result)
      print("\n")

   elif (x == 2):
      s = int(input("Enter Business ID <integer> : "))
      result = contract.functions.getBusinessBalance(s).call()
      print(result)
      print("\n")

   elif (x == 3):
      s = int(input("Enter business ID <integer> : "))
      print("Formated user id : ",s)
      try:
         result = contract.functions.getBusinessBalance(s).call()
         transaction = contract.functions.resetBusinessBalance(s).buildTransaction({
             'gas': 2000000,
             'gasPrice': w3.toWei('50', 'gwei'),
             'nonce': w3.eth.getTransactionCount(sender_address),
         })

         # Sign and send the transaction
         signed_txn = w3.eth.account.signTransaction(transaction, private_key='1bc9616d0c1916ae1f32d0af29e88fb41eb01db2a16371bbe821f752b3d21d7a')
         tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

         print(tx_hash)
         print(f"Transaction Completed successfully. Balance reduced from {result} to 0.")
         print("\n")
      except:
         print("Transaction Failed")
         print("\n")


   elif (x == 4):
      s = input("Enter user ID : ")
      s = s.replace(" ","")
      s = s.lower()
      print("Formated user id : ",s)
      try: 
         transaction = contract.functions.addUser(s).buildTransaction({
             'gas': 2000000,
             'gasPrice': w3.toWei('50', 'gwei'),
             'nonce': w3.eth.getTransactionCount(sender_address),
         })

         # Sign and send the transaction
         signed_txn = w3.eth.account.signTransaction(transaction, private_key='1bc9616d0c1916ae1f32d0af29e88fb41eb01db2a16371bbe821f752b3d21d7a')
         tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

         print(tx_hash)
         print("User Registered successfully.")
         print("\n")
      except:
         print("Failed to add User")
         print("\n")

   elif (x == 5):
      s = input("Enter user ID : ")
      x = int(input("Enter amount to be added <integer> : "))
      s = s.replace(" ","")
      s = s.lower()
      print("Formated user id : ",s)
      try: 
         transaction = contract.functions.addBalanceToUser(s,x).buildTransaction({
             'gas': 2000000,
             'gasPrice': w3.toWei('50', 'gwei'),
             'nonce': w3.eth.getTransactionCount(sender_address),
         })

         # Sign and send the transaction
         signed_txn = w3.eth.account.signTransaction(transaction, private_key='1bc9616d0c1916ae1f32d0af29e88fb41eb01db2a16371bbe821f752b3d21d7a')
         tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

         print(tx_hash)
         print("User Registered successfully.")
         print("\n")
      except:
         print("Failed to add User")
         print("\n")

   elif (x == 6):
      s = int(input("Enter Business ID <integer> : "))
      n = input("Enter Business Name : ")
      try: 
         transaction = contract.functions.addBusiness(s).buildTransaction({
             'gas': 2000000,
             'gasPrice': w3.toWei('50', 'gwei'),
             'nonce': w3.eth.getTransactionCount(sender_address),
         })

         # Sign and send the transaction
         signed_txn = w3.eth.account.signTransaction(transaction, private_key='1bc9616d0c1916ae1f32d0af29e88fb41eb01db2a16371bbe821f752b3d21d7a')
         tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        
         print(tx_hash)
         
         st = "INSERT INTO data(business_ID,business_Name) values('{}','{}')".format(s,n)
         cur.execute(st)
         conn.commit()
         print("Business Registered successfully.")
         print("\n")
      except:
         print("Failed to add Business")
         print("\n")

   elif (x == 7):
      s = int(input("Enter Business ID <integer> : "))
      a = int(input(' Enter amount to be added <integer> : '))
      try: 
         transaction = contract.functions.addBalanceToBusiness(s,a).buildTransaction({
             'gas': 2000000,
             'gasPrice': w3.toWei('50', 'gwei'),
             'nonce': w3.eth.getTransactionCount(sender_address),
         })

         # Sign and send the transaction
         signed_txn = w3.eth.account.signTransaction(transaction, private_key='1bc9616d0c1916ae1f32d0af29e88fb41eb01db2a16371bbe821f752b3d21d7a')
         tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        
         print(tx_hash)
         print("Transaction completed successfully.")
         print("\n")
      except:
         print("Transaction Failed!")
         print("\n")


   elif (x == 8):
      s = input("Enter user ID : ")
      b = int(input("Enter business ID <integer> : "))
      x = int(input("Enter amount to be added <integer> : "))
      s = s.replace(" ","")
      s = s.lower()
      print("Formated user id : ",s)
      try: 
         transaction = contract.functions.transferBalanceFromUserToBusiness(s,b,x).buildTransaction({
             'gas': 2000000,
             'gasPrice': w3.toWei('50', 'gwei'),
             'nonce': w3.eth.getTransactionCount(sender_address),
         })

         # Sign and send the transaction
         signed_txn = w3.eth.account.signTransaction(transaction, private_key='1bc9616d0c1916ae1f32d0af29e88fb41eb01db2a16371bbe821f752b3d21d7a')
         tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

         print(tx_hash)
         print("Transaction Completed Successfully.")
         print("\n")
      except:
         print("Transaction Failed!")
         print("\n")
         
   elif(x == 9):
      cur.execute("select * from data")
      Business_data = cur.fetchall()
      count = cur.rowcount
      print(" No. of businesses : ",count)
      for i in Business_data:
         print(i)

      print("\n")


      
      

