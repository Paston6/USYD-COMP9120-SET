#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

'''
Connect to the database using the connection string
'''
def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    #userid = "y21s1c9120_xxin7882"
    #passwd = "xx199881"
    #myHost = "soit-db-pro-2.ucc.usyd.edu.au"
    userid = "postgres"
    db = "postgres"
    passwd = "md5d8364ff6268b88f58555916dd370450e"
    myHost = "localhost"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=db,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn

'''
Validate a sales agent login request based on username and password
'''
def checkUserCredentials(userName, password):
    # TODO - validate and get user info for a sales agent


    userInfo = ['2', 'novak', 'Novak', 'Djokovic', '222']

    return userInfo


'''
List all the associated bookings in the database for a given sales agent Id
'''
def findBookingsBySalesAgent(agentId):
    # TODO - list all the associated bookings in DB for a given sales agent Id

    booking_db = [
        ['1', 'Bob Smith', 'The Lion King', '2021-06-05', 'Novak Djokovic', 'I\'d like to book 3 additional seats'],
        ['5', 'Mia Clark', 'Disney\'s Frozen', '2021-07-18', 'Novak Djokovic', 'Please upgrade my seats to Box Seats'],
        ['3', 'Ruby Miller', 'Death of a Salesman', '2021-06-27', 'Novak Djokovic', 'I want to add meals to my booking']
    ]

    booking_list = [{
        'booking_no': row[0],
        'customer_name': row[1],
        'performance': row[2],
        'performance_date': row[3],
        'booked_by': row[4],
        'instruction': row[5]
    } for row in booking_db]

    return booking_list


'''
Find a list of bookings based on the searchString provided as parameter
See assignment description for search specification
'''
def findBookingsByCustomerAgentPerformance(searchString):
    # TODO - find a list of bookings in DB based on searchString input

    booking_db = [
        ['1', 'Bob Smith', 'The Lion King', '2021-06-05', 'Novak Djokovic', 'I\'d like to book 3 additional seats'],
        ['4', 'Peter Wood', 'The Lion King', '2021-06-05', 'Jeff Alexander', 'Can you please waitlist 4 seats?']
    ]

    booking_list = [{
        'booking_no': row[0],
        'customer_name': row[1],
        'performance': row[2],
        'performance_date': row[3],
        'booked_by': row[4],
        'instruction': row[5]
    } for row in booking_db]

    return booking_list


#####################################################################################
##  Booking (customer, performance, performance date, booking agent, instruction)  ##
#####################################################################################
'''
Add a new booking into the database - details for a new booking provided as parameters
'''
def addBooking(customer, performance, performance_date, booked_by, instruction):
    # TODO - add a booking
    # Insert a new booking into database
    # return False if adding was unsuccessful
    # return True if adding was successful

    return True


'''
Update an existing booking with the booking details provided in the parameters
'''
def updateBooking(booking_no, performance, performance_date, booked_by, instruction):
    # TODO - update an existing booking in DB
    # return False if updating was unsuccessful
    # return True if updating was successful

    return True

openConnection()

