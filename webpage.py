from flask import Flask
from flask import request
from flask import render_template
import json
import datetime
from pymongo import MongoClient

# Connecting to mongodb
client = MongoClient('mongodb://localhost:27017/')
# Telling mongo to retrieve db named DATABASENAME
db = client.CSCFinalProject
# Telling mongo to retrieve collection named COLLECTIONNAME
collection = db.Project1


app = Flask(__name__)

# Function that determines if TIME is between START TIME and END TIME
# Used in search to add 45 min margin
def is_hour_between(start, end, time):
    is_between = False
    is_between |= start <= time <= end
    is_between |= end < start and (start <= time or time <= end)
    return is_between

@app.route('/', methods=['GET'])
def index():
    # Parsing data from MongoDb
    for x in collection.find():
        data = x
    # Rendering Template index.html and passing data from MongoDb
    return render_template('index.html',data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Parsing data from MongoDb
    for x in collection.find():
        data = x

    # Executes only if the search input is filled and submited
    if request.method == 'POST':
        # Preparing empty dictionary for search
        emptyDict = {'room_day_template': [{}]}
        # Get value of the search input
        timeReq = request.form.get('time')
        # Formatting the input value to H:m format
        timeFormat = datetime.datetime.strptime(timeReq,'%H:%M')
        # Lower margin for search (time input value - 45 mins)
        minTime = timeFormat-datetime.timedelta(minutes=45)
        # Higher margin for search (time input value + 45 mins)
        maxTime = timeFormat+datetime.timedelta(minutes=45)

        # Parsing data from mongodb
        for dat in data['room_day_template']:
            for x in dat['stateAtTime']:
                # Calling is_hour_between function with margins to check if input time is between margins
                if is_hour_between(minTime, maxTime, datetime.datetime.strptime(x['time'], '%H:%M')):
                    # Appending data that matches search to the emptyDict for frontend display
                    emptyDict['room_day_template'].append({
                        "name": dat['name'],
                        "id": dat['id'],
                        "stateAtTime": [x]
                        })
        # Passing time input back to the template for use as value in the input
        emptyDict['time'] = timeReq
        # Return search.html with emptyDict data
        return render_template('search.html',data=emptyDict)
    else:
        data = ''
        return render_template('search.html',data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    # Asigning $_GET variable to p_id
    p_id = int(request.args.get('id'))
    # Fetching data from DB
    for x in collection.find():
        data = x
    if request.method == 'POST':
        # Getting value from hidden time input for identifying stateAtTime to edit
        timeReq = request.form.get('time')
        # Validating that we want to add roomObject with the dataToChange hidden input
        if request.form.get('dataToChange') == 'roomObject':
            # Getting roomObject from $_POST request
            roomObjectReq = request.form.get('roomObject')
            arr = []
            # Looping the DB data 
            db_id = 0
            for dat in data['room_day_template']:
                # If database id matches $_GET['id'] we loop the stateAtTime object
                if p_id == dat['id']:
                    for x in range(len(dat['stateAtTime'])):
                        # Checking if stateAtTime.time is equal with the time input looking for the right time to update
                        if dat['stateAtTime'][x]['time'] == timeReq:
                            # Saving intended stateAtTime goodIndex
                            goodTime = x
                            # Saving oldRoomObjects for later search in database
                            oldRoomObjects = dat['stateAtTime'][x]['roomState']['room_objects']
                            # Making a copy of oldRoomObjects
                            newRoomObjects = oldRoomObjects.copy()
                            # Append the value from the room object input to the newRoomObjects object
                            newRoomObjects.append(roomObjectReq)
                            # Searching the database for the old data and replace with new roomObjects
                            collection.update_one({
                                    "room_day_template."+str(db_id)+".stateAtTime."+str(x)+".roomState.room_objects" : oldRoomObjects
                                },{
                                '$set' : {
                                    "room_day_template."+str(db_id)+".stateAtTime."+str(x)+".roomState.room_objects" : newRoomObjects
                                }
                            })
                    # Update the original data from db array with the new room objects
                    dat['stateAtTime'][goodTime]['roomState']['room_objects'] = newRoomObjects
                    # Append the correct data to empty array for frontend rendering
                    arr.append(dat)
                db_id += 1
            return render_template('add.html', data=arr)
        
        # Validating that we want to add objectState with the dataToChange hidden input
        elif request.form.get('dataToChange') == 'objectState':
            # Initializing variables with data from $_POST request
            objectName = request.form.get('objectName')
            objectId = request.form.get('objectId')
            objectAction = request.form.get('objectAction')
            objectBool = request.form.get('objectBool')
            arr = []
            # Looping database, searching for matching id
            db_id = 0
            for dat in data['room_day_template']:
                # If database id matches $_GET['id'] we loop the stateAtTime object
                if p_id == dat['id']:
                    for x in range(len(dat['stateAtTime'])):
                        # Checking if stateAtTime.time is equal with the time input looking for the right time to update
                        if dat['stateAtTime'][x]['time'] == timeReq:
                            # Saving intended stateAtTime goodIndex
                            goodTime = x
                            # Saving oldRoomObjects for later search in database
                            oldRoomObjectState = dat['stateAtTime'][x]['objectState']
                            # Making a copy of oldRoomObjectsStates
                            newRoomObjectState = oldRoomObjectState.copy()
                            # Append the value from the room object input to the newRoomObjectsStates object
                            newRoomObjectState.append({
                                "object_name": objectName,
                                "object_id": objectId,
                                objectAction: objectBool
                            })
                            # Searching the database for the old data and replace with new objectStates
                            collection.update_one({
                                    "room_day_template."+str(db_id)+".stateAtTime."+str(x)+".objectState" : oldRoomObjectState
                                },{
                                '$set' : {
                                    "room_day_template."+str(db_id)+".stateAtTime."+str(x)+".objectState" : newRoomObjectState
                                }
                            })
                            # Update the original data from db array with the new room objects states
                            dat['stateAtTime'][goodTime]['objectState'] = newRoomObjectState
                            # Append the correct data to empty array for frontend rendering
                            arr.append(dat)
                db_id += 1
            return render_template('add.html', data=arr)
        elif request.form.get('dataToChange') == 'role':
            # Initializing variables with data from $_POST request
            roleName = request.form.get('roleName')
            roleId = request.form.get('roleId')
            roleObjectId = request.form.get('roleObjectId')
            roleAction = request.form.get('roleAction')
            arr = []
            # Looping database, searching for matching id
            db_id = 0
            for dat in data['room_day_template']:
                # If database id matches $_GET['id'] we loop the stateAtTime object
                if p_id == dat['id']:
                    for x in range(len(dat['stateAtTime'])):
                        # Checking if stateAtTime.time is equal with the time input looking for the right time to update
                        if dat['stateAtTime'][x]['time'] == timeReq:
                            # Saving intended stateAtTime goodIndex
                            goodTime = x
                            # Saving oldRoles for later search in database
                            oldRoomRoles = dat['stateAtTime'][x]['role']
                            # Making a copy of oldRoomObjectsStates
                            newRoomRoles = oldRoomRoles.copy()
                            # Append the value from the room object input to the newRoomRoles object
                            newRoomRoles.append({
                                "role_name": roleId,
                                "role_id": roleId,
                                "role_object_id": [roleObjectId],
                                "role_action": [roleAction]
                            })
                            # Searching the database for the old data and replace with new objectStates
                            collection.update_one({
                                    "room_day_template."+str(db_id)+".stateAtTime."+str(x)+".role" : oldRoomRoles
                                },{
                                '$set' : {
                                    "room_day_template."+str(db_id)+".stateAtTime."+str(x)+".role" : newRoomRoles
                                }
                            })
                            # Update the original data from db array with the new room objects states
                            dat['stateAtTime'][goodTime]['role'] = newRoomRoles
                            # Append the correct data to empty array for frontend rendering
                            arr.append(dat)
                db_id += 1
            return render_template('add.html', data=arr)
    # If method == 'GET'
    else:
        arr = []
        # Looping the database
        for dat in data['room_day_template']:
            # Searching the object id that matches with GET request's id
            if p_id == dat['id']:
                # Appending to array for frontend rendering
                arr.append(dat)
                break
        # Return data to frontend
        return render_template('add.html', data=arr)

    

    

@app.route('/raw')
def raw():
    # Loop the database and save all data to the data variable
    for x in collection.find():
        data = x
    # Renders raw data to frontend
    return json.dumps(data['room_day_template'])

if __name__ == '__main__':
    app.run(debug=True)