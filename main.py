import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.environ["DB_URL"]

cred = credentials.Certificate(db_url)

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def signIn(username="", password=""):
  print(f"UN: {username} PW: {password}")
  if username and password:
    return (username, password, True)
  while True:
    # Prompt for username and password
    username = input("What is your username?: ")
    password = input("What is your password?: ")

    # Call authorizeUser to check if username and password are correct
    authState = authorizeUser(username, password)

    # If authorization is successful, break the loop
    if authState:
      return (username, password, authState)
    else:
      print("\nInvalid username or password. Please try again.\n")


def authorizeUser(uN, pW):
  # Retrieve the document data for the provided username
  doc = getDoc(uN)

  # Check if the username exists
  if doc.exists:
    # Get the document data as a dictionary
    data = doc.to_dict()

    # Ensure the 'password' field exists
    if 'password' in data:
        # Compare the provided password (pW) with the stored password
        if data['password'] == pW:
          print("\nAuthorization successful!\n")
          return True  # Passwords match
        else:
          print("\nIncorrect password.\n")
          return False  # Incorrect password
    else:
      print(f"\nPassword field not found for user: {uN}.\n")
      return False  # Password field missing
  else:
    print(f"\nNo document found for username: {uN}.\n")
    return False  # Username does not exist

def viewData(username):
  doc = getDoc(username)
  
  if doc.exists:
    # Get the document data as a dictionary
    data = doc.to_dict()

    # Remove the 'password' field if it exists
    if 'password' in data:
      data.pop('password')
    
    # Print the document data without the password
    print(f"\n{doc.id} => {data}\n")
  else:
    # If the document doesn't exist, print an error message
    print(f"\nNo document found for username: {username}\n")



def updateData(uN):
  viewData(uN)
  documentToUpdate = input("Which document would you like to update?: ")

  udatedData = input("What is the status of this application?: ")


  doc_ref = getDocRaw(uN)
  doc_ref.update({documentToUpdate: udatedData})

def addApplication(uN):
  companyName = input("What is the name of the company that you applied for?: ")
  statusOfApplication = input("What is the status of the application?: ")
  doc_ref = getDocRaw(uN)
  doc_ref.update({companyName: statusOfApplication})
  return

def createAccount():
  userName = input("What is your username?: ")
  doc = getDoc(userName).to_dict()
  if not doc:
    while True:
      password1 = input("What is your password?: ")
      password2 = input("Confirm your password: ")

      if password1 != password2:
        print('passwords do not match, please try again')
      else:
        getDocRaw(userName).set({
        "password": password2
        })
        print("\nAccount Created!\n")
        return signIn(userName, password2)
        break
  else:
    print("\nThat username already exists!\n")

def getDoc(username):
  return db.collection("test1").document(f"{username}").get()

def getDocRaw(username):
  return db.collection("test1").document(f"{username}")


def main():
  credentials = ""
  while True:
    print("Menu:")
    print("1. Sign In")
    print("2. Create an Account")
    print("3. View Data")
    print("4. Add Application and Status")
    print("5. Update Data")
    print("6. Sign Out")
    print("7. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
      #  sign in
      credentials = signIn()
    elif choice == '2':
      # if you are not signed in, you can create an account
      if not credentials:
        credentials = createAccount()
      else:
        credentials = ""
        print("\nYou must sign out before creating a new account!\n")
    elif choice == '3':
      # Are you signed in?
      if credentials:
        viewData(credentials[0])
      else:
        print("\nYou must sign in before viewing data!\n")
    elif choice == '4':
      # Are you signed in?
      if credentials:
        addApplication(credentials[0])
      else:
        print('\nYou must sign in before adding data!\n')
    elif choice == '5':
      # Are you signed in?
      if credentials:
        updateData(credentials[0])
      else:
        print('\nYou must sign in before updating data!\n')
    elif choice == '6':
      # Are you signed in?
      if credentials:
        credentials = ""
        print("\nsuccessfully logged out\n")
      else:
        print('\nYou are not signed in!\n')
    elif choice == '7':
      print("Exiting...")
      break
    else:
      print("Invalid choice. Please enter a number between 1 and 4.")

main()