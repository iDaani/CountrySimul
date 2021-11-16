# CountrySimulation

The main vision of this project is to simulate a real-life state of the country akin to a video game that will be able to store the lives and updates of citizens of a country, the objects as well as their states over some years. We aim to store this simulation in an efficient way so it can be easily handled and queried in a normal PC.


## How do we implement this idea?

> We create JSON templates that store life-like visualisations of a state of a room object at a particular time. Say 3 PM; we will store what the state of the room at 3 PM is that is - 
> * the objects in the room like chair, lights with a name, unique ID 
> * the roles that is the people in the room with a name, unique ID
> * Object states that include what is the state of an object like if a light is turned on or off. This is stored in boolean.
> * Roles states that include what the role is doing aka an action. Such as they're sitting, watching.
> * Roles associated with Objects includes the ID of the object that the role is associated with. Like if their action is sitting, the object ID will tell where the role is sitting on.
> 

This allows almost real-life visualisations to how a single room is changing over state of time. At this stage, we have limited it to just a few rooms but this can be expanded upon - to even include years!

## Further more information

For more detailed information about the project, read the following:
* **How-to guide** - https://github.com/iDaani/CountrySimulation/blob/main/Web/howtoguide.html - Shows in detail every part of the project and how to get a grasp of the project as a starter to run it.
* **Project summary** - https://github.com/iDaani/CountrySimulation/blob/main/Web/websummary.html - Summarizes what the project is about and we're trying to achieve and have achieved.
## Beginning with the project

To begin with the project, first read the requirements over **https://github.com/iDaani/CountrySimulation/blob/main/requirements.md**

Download the required applications and libraries for easy implementation of the project.

## How to run this project

* Make changes to 'upload_final.py' and 'webpage.py' with your MongoDB database details.
> In case you have a MongoDB database with username and password, change the connection line code to ```python
> client = MongoClient('mongodb://%s:%s@IPADRESS:27017' % ('USERNAME HERE', 'PASSWORD HERE'))
> ```

* Run 'upload_final.py' to upload the JSON template to the MongoDB Collection.
* Run 'webpage.py' to start the Flask webserver.
* Open the flask webserver to access the webpage.

## Has this project been tested with test code?

Yes, the sample test data is already present when you run the project. It has been tested already with test cases which you can read from https://github.com/iDaani/CountrySimulation/blob/main/Web/Codes/Testing%20Template.xlsx


