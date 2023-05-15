from flask import Flask, request, render_template
from flask import jsonify
import vobject
import json
from pymongo import MongoClient
import pymongo
import certifi
from bson import json_util
from flask import Response
from bson import json_util
from flask_cors import CORS
import os
import requests

API_KEY = "admin0"

#test 

print("hei")
# print(json_text)



#mongodb+srv://vegardstamadsen:zvNcYlvVwuE1ScJv@cluster0.bomsogj.mongodb.net/test
try:
    
    client = pymongo.MongoClient("mongodb+srv://vegardstamadsen:zvNcYlvVwuE1ScJv@cluster0.bomsogj.mongodb.net/test", tlsCAFile=certifi.where())
    print("Connected to MongoDB")

   
    mydb = client["CloudContacts"]

   
    mycol = mydb["Contacts"]

  

except Exception as e:
    print(f"Could not connect to MongoDB: {e}")



app = Flask("Api")
cors = CORS(app)


# Simulated database
CONTACTS =[]
contactsMy = []
contacts = []


# Load the JSON data from file







@app.route('/')
def hello():
    
    return 'Velkommen til vår API'
    
    



# Settings
MyData = []

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    if request.headers.get('admin0') != API_KEY:
        return jsonify({'message': 'Invalid API key'})

    
   
    if request.method == 'POST':
        file = request.files['file']
        file_content = file.read().decode('utf-8')
        text = vobject.readComponents(file_content)


        
        for dataContact in text:
            
            phone = "--No Information--"
            try:
                phone = str(dataContact.tel.value)
            except AttributeError:
                pass
            
            address = "--No Information--"
            try:
                address = str(dataContact.adr.value)
            except AttributeError:
                pass

            company = "--No Information--"
            try:
                company = str(dataContact.org.value[0])
            except AttributeError:
                pass


            MyContact = {
                'email': dataContact.email.value,
                'name': str(dataContact.n.value),
                'fullname': dataContact.fn.value,
                'address': address,
                'company': company,
                'phone': phone,
 
            }

            
            result = mycol.insert_one(MyContact)
            MyData.append(str(result.inserted_id))
            print(MyContact)

             # Trigger an update request to the cache server
        cache_url = "http://localhost:5555/update_cache"
        response = requests.get(cache_url)

        return jsonify({'message': MyData}) 
        
    else:
        # show the upload form
        return render_template('upload.html')
        
    
@app.route('/contacts/vcard')

def get_contacts_vcard():


    try:
        
        contacts = list(mycol.find())

        
        vcard_data = []

        
        for contact in contacts:
            
            name = contact['name']
            address = contact['address']
            organization = contact.get('organization', '')
            phone = contact.get('phone', '')
            email = contact.get('email', '')

            
            vcard_string = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nN:{name};;;;\nORG:{organization}\nADR:;;;;{address}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD\n"

            
            vcard_data.append({'vcard': vcard_string})

       
        return jsonify(vcard_data)
    except Exception as e:
        # log the error
        print(f"An error occurred: {str(e)}")
        # return a 500 error response
        return Response(status=500)

@app.route('/contacts/vcard/<email>')
def get_specific_vcard(email):
    try:
        
        contact = mycol.find_one({'email': email})

        if contact is not None:
            
            name = contact['name']
            address = contact['address']
            organization = contact.get('organization', '')
            phone = contact.get('phone', '')
            email = contact.get('email', '')

            
            vcard_string = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nN:{name};;;;\nORG:{organization}\nADR:;;;;{address}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD\n"

            
            return jsonify({'vcard': vcard_string})
        else:
            
            return Response(status=404)
    except Exception as e:
        
        print(f"An error occurred: {str(e)}")
        
        return Response(status=500)   

@app.route('/contacts')
def get_contacts():
   
    contacts = []

    
    for contact in mycol.find():
    
        contact = json.loads(json_util.dumps(contact))
        contacts.append(contact)

    
    return jsonify(contacts)

@app.route('/contacts/<email>')
def get_contact(email):
    
    contact = mycol.find_one({'email': email})

    if contact is not None:
        
        contact = json.loads(json_util.dumps(contact))
        return jsonify(contact)
    else:
        return f"Contact with email {email} does not exist"


 


@app.route('/contacts', methods=['POST'])
def create_contact():
    
    name = request.json['name']
    address = request.json['address']

   
    contact = {'name': name, 'address': address}


    result = mycol.insert_one(contact)

    
    return {'id': str(result.inserted_id)}


@app.route('/contacts/<id>', methods=['DELETE'])
def delete_contact(id):
    del CONTACTS[int(id)]
    return  {'id': id}

@app.route('/contacts/export')
def export_contacts():
    try:
        
        contacts = list(mycol.find())

        
        vcard_data = []

        
        for contact in contacts:
           
            name = contact['name']
            address = contact['address']
            organization = contact.get('company', '')
            phone = contact.get('phone', '')
            email = contact.get('email', '')

            
            vcard_string = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nN:{name};;;;\nORG:{organization}\nADR:;;;;{address}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD\n"

            
            vcard_data.append(vcard_string)

        
        vcard_file_contents = "\n".join(vcard_data)

        
        filename = "contacts.vcf"

        
        response = Response(vcard_file_contents, mimetype='text/x-vcard')
        response.headers.set("Content-Disposition", f"attachment; filename={filename}")
        print(vcard_file_contents)
        return response
    except Exception as e:
       
        print(f"An error occurred: {str(e)}")
       
        return Response(status=500)



if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=6438)
