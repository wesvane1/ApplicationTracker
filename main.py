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


def updateStatus(uN):
  viewData(uN)
  documentToUpdate = input("Which document would you like to update?: ")

  # Get the document reference and fetch the current status
  doc_ref = getDocRaw(uN)
  current_data = doc_ref.get()
  
  # Retrieve the old status from the document
  old_status = current_data.get(documentToUpdate)

  # Prompt for the new status
  updatedData = input("What is the status of this application?: ")

  # Update the document with the new status
  doc_ref.update({documentToUpdate: updatedData})

  # Print the old and new status
  print(f"\n{documentToUpdate} has been updated from '{old_status}', to '{updatedData}'\n")




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

def updateCompanyName(username, old_field, new_field):
  # Reference to the document (replace 'test1' with your actual collection name)
  data_raw = getDocRaw(username)
  
  # Get the document data
  doc = data_raw.get()
  
  if doc.exists:
    # Convert the document to a dictionary
    data = doc.to_dict()

    # Check if the old field exists
    if old_field in data:
      # Update the document with the corrected field name
      data_raw.update({
        new_field: data[old_field],  # Copy the value from old_field to new_field
        old_field: firestore.DELETE_FIELD  # Delete the old field
      })
      print(f"\nField '{old_field}' has been changed to '{new_field}'.\n")
    else:
      print(f"\nField '{old_field}' does not exist in the document.\n")
  else:
    print(f"\nDocument with ID {username} does not exist.\n")

def getDoc(username):
  return db.collection("test1").document(f"{username}").get()

def getDocRaw(username):
  return db.collection("test1").document(f"{username}")

def updateOptions(username):
  viewData(username)
  while True:
    print("\nUpdate Data Menu:")
    print("1. Update Company Name")
    print("2. Update Status")
    print("3. Go Back")

    update_choice = input("Enter your choice (1-3): ")

    if update_choice == '1':
      oldCompanyName = input("Enter the name you want to change: ")
      newCompanyName = input("Enter the new company name: ")
      updateCompanyName(username, oldCompanyName, newCompanyName)
      viewData(username)
      break
    elif update_choice == '2':
      updateStatus(username)
      # Add logic here to update the status in your data structure
    elif update_choice == '3':
      print("\nReturning to main menu...\n")
      break
    else:
      print("\nInvalid choice. Please enter a number between 1 and 3.\n")


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

    choice = input("Enter your choice (1-7): ")

    if choice == '1':
      #  sign in
      credentials = signIn()
    elif choice == '2':
      # if you are not signed in, you can create an account
      if not credentials:
        credentials = createAccount()
      else:
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
        updateOptions(credentials[0])
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
      print("Invalid choice. Please enter a number between 1 and 7.")

main()