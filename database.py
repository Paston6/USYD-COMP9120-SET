#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################
def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    
    # leave empty for submission
    userid = "postgres"
    passwd = "xx199881"
    myHost = "localhost"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid, user=userid, password=passwd, host=myHost)
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)

    # return the connection to use
    return conn

#####################################################
##  Database fetching function 
#####################################################

# ====================================================================
# Validate a sales agent login request based on username and password
# ====================================================================
def checkUserCredentials(userName, password):
    # Open connection
    conn = openConnection()
    cursor = conn.cursor()
    
    # Execute SQL script
    cursor.execute("select * from AGENT where USERNAME = \'" + userName + "\';")
    res = cursor.fetchone()

    # If password not correct return None
    if (res == None):
        return None
    elif(res[4] == password):
        return list(res)
    
    # If password not correct return None
    return None


# ============================================================================
# List all the associated bookings in the database for a given sales agent Id
# ============================================================================
def findBookingsBySalesAgent(agentId):
    # Open connection
    conn = openConnection()
    cursor = conn.cursor()
    
    # execute sql query
    sql_query = "select booking_no,concat(customer.firstname,' ', customer.lastname) as customer_name,performance,performance_date,agent_name,instruction from \
        (select booking_no,customer,performance, performance_date,concat(firstname,' ',lastname) as agent_name,instruction \
        from booking left join agent on booking.booked_by = agent.agentid \
        where booking.booked_by = " + str(agentId) + ") as A \
        left join customer on A.customer = customer.email order by customer_name ASC;"
    cursor.execute(sql_query)

    # Fetch all data
    booking_db = []
    while(True):
        record = cursor.fetchone()
        if record == None:
            break
        else:
            booking_db.append(list(record))

    # if no result found return None
    if (len(booking_db) < 1):
        return None

    # rebuild booking list 
    booking_list = [{
        'booking_no': str(row[0]),
        'customer_name': row[1],
        'performance': row[2],
        'performance_date': row[3],
        'booked_by': row[4],
        'instruction': row[5]
    } for row in booking_db]

    return booking_list


# =========================================================================
# Find a list of bookings based on the searchString provided as parameter
# See assignment description for search specification
# =========================================================================
def findBookingsByCustomerAgentPerformance(searchString):
    # Open connection
    conn = openConnection()
    cursor = conn.cursor()

    # find result
    sql_query = "select * from \
        (select BOOKING_NO, concat(customer.firstname,' ',customer.lastname) as customer_name, performance, \
        performance_date, concat(Book_agent.firstname,' ',Book_agent.lastname) as agent_name, instruction \
        from (select * from booking left join agent on booking.booked_by = agent.agentid) as Book_agent \
        left join customer on Book_agent.customer = customer.email ) as book_agent_customer \
        where lower(customer_name) like '%" + searchString.lower() + "%' \
        or lower(performance) like '%" + searchString.lower() + "%' \
        or lower(agent_name) like '%" + searchString.lower()  + "%' \
        order by customer_name ASC;"
    cursor.execute(sql_query)

    # Fetch all data
    booking_db = []
    while(True):
        record = cursor.fetchone()
        if record == None:
            break
        else:
            booking_db.append(list(record))

    # if no result found return None
    if (len(booking_db) < 1):
        return None

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
    # setup connection
    conn = openConnection()
    cursor = conn.cursor()
    # if booked_by is number dont use trigger else use trigger to find agent name 
    if (booked_by.isnumeric()):
        print("yes")
        sql_query = "INSERT INTO BOOKING (CUSTOMER,PERFORMANCE,PERFORMANCE_DATE,BOOKED_BY,INSTRUCTION) \
                 values ($$"+customer+"$$,$$"+performance+"$$,$$"+performance_date+"$$,"+str(booked_by)+",$$"+instruction+"$$);"
    else:
        print("no")
        sql_query = "INSERT INTO BOOKING (CUSTOMER,PERFORMANCE,PERFORMANCE_DATE,BOOKED_BY,INSTRUCTION) \
                 values ($$"+customer+"$$,$$"+performance+"$$,$$"+performance_date+"$$,get_booked_by($$"+str(booked_by)+"$$),$$"+instruction+"$$);"

    # Insert a new booking into database
    try:
        cursor.execute(sql_query)
    except psycopg2.Error as sqle:
        conn.rollback()
        return False

    # save changes and return success
    conn.commit()
    conn.close()
    return True

'''
Update an existing booking with the booking details provided in the parameters
'''
def updateBooking(booking_no, performance, performance_date, booked_by, instruction):
    # setup connection
    conn = openConnection()
    cursor = conn.cursor()

    # update sql query (used $$ just incase if ' in string')
    sql_query =  "UPDATE BOOKING \
    SET PERFORMANCE = $$"+str(performance)+"$$,PERFORMANCE_DATE = $$"+str(performance_date)+ "$$, \
    BOOKED_BY = get_booked_by($$"+str(booked_by)+"$$), INSTRUCTION = $$"+str(instruction)+"$$ \
    WHERE BOOKING_NO = "+str(booking_no)+";"

    # Insert a new booking into database
    try:
        cursor.execute(sql_query)
    except psycopg2.Error as sqle:
        conn.rollback()
        return False

    # save changes and return success
    conn.commit()
    conn.close()
    return True



























# =================================
#  BackUp: AUTO generate Database
# =================================
'''
sql = """
DROP TABLE IF EXISTS BOOKING;
DROP TABLE IF EXISTS CUSTOMER;
DROP TABLE IF EXISTS AGENT;

-- Set time style to DD/MM/YYYY --
-- (Since at the back it is something like 07/06/2021) --
SET datestyle = DMY;

CREATE TABLE AGENT
(
    AGENTID SERIAL PRIMARY KEY,
    USERNAME VARCHAR(20) NOT NULL UNIQUE,
    FIRSTNAME VARCHAR(50) NOT NULL,
    LASTNAME VARCHAR(50) NOT NULL,
    PASSWORD VARCHAR(20) NOT NULL
);

INSERT INTO AGENT (USERNAME,FIRSTNAME,LASTNAME,PASSWORD) VALUES ('-','N/A','','111');
INSERT INTO AGENT (USERNAME,FIRSTNAME,LASTNAME,PASSWORD) VALUES ('novak','Novak','Djokovic','222');
INSERT INTO AGENT (USERNAME,FIRSTNAME,LASTNAME,PASSWORD) VALUES ('jeff','Jeff','Alexander','333');
INSERT INTO AGENT (USERNAME,FIRSTNAME,LASTNAME,PASSWORD) VALUES ('marie','Mariana','Johnson','444');
INSERT INTO AGENT (USERNAME,FIRSTNAME,LASTNAME,PASSWORD) VALUES ('xing','Xing','Xing','555');

CREATE TABLE CUSTOMER
(
    EMAIL VARCHAR(50) PRIMARY KEY,
    FIRSTNAME VARCHAR(50) NOT NULL,
    LASTNAME VARCHAR(50) NOT NULL,
    -- check user email is legal --
    CONSTRAINT valid_email CHECK (EMAIL ~ '^[A-Za-z0-9.%_-|,+*&^$#]+@[A-Za-z0-9]+[.][A-Za-z]+$')
);

INSERT INTO CUSTOMER (EMAIL,FIRSTNAME,LASTNAME) VALUES ('bobsmith11@gmail.com','Bob','Smith');
INSERT INTO CUSTOMER (EMAIL,FIRSTNAME,LASTNAME) VALUES ('abrown87@outlook.com','Anthony','Brown');
INSERT INTO CUSTOMER (EMAIL,FIRSTNAME,LASTNAME) VALUES ('ruby.m5@gmail.com','Ruby','Miller');
INSERT INTO CUSTOMER (EMAIL,FIRSTNAME,LASTNAME) VALUES ('woodp88@yahoo.com','Peter','Wood');
INSERT INTO CUSTOMER (EMAIL,FIRSTNAME,LASTNAME) VALUES ('m.clark12@gmail.com','Mia','Clark');
INSERT INTO CUSTOMER (EMAIL,FIRSTNAME,LASTNAME) VALUES ('jamie_ol@gmail.com','Jamie','Oliver');
INSERT INTO CUSTOMER (EMAIL,FIRSTNAME,LASTNAME) VALUES ('anny@gmail.com','Anny','Wong');

CREATE TABLE BOOKING
(
    BOOKING_NO SERIAL PRIMARY KEY,
    CUSTOMER VARCHAR(50) NOT NULL REFERENCES CUSTOMER,
    PERFORMANCE VARCHAR(100) NOT NULL,
    PERFORMANCE_DATE DATE NOT NULL,
    BOOKED_BY INTEGER NOT NULL REFERENCES AGENT,
    INSTRUCTION VARCHAR(200),
    -- booking performing time have to be in the future --
    CONSTRAINT valid_performance_time CHECK (PERFORMANCE_DATE > now())
);

INSERT INTO BOOKING (CUSTOMER,PERFORMANCE,PERFORMANCE_DATE,BOOKED_BY,INSTRUCTION) values ('bobsmith11@gmail.com','The Lion King','05/09/2021',2,'I''d like to book 3 additional seats');
INSERT INTO BOOKING (CUSTOMER,PERFORMANCE,PERFORMANCE_DATE,BOOKED_BY,INSTRUCTION) values ('abrown87@outlook.com','Romeo & Juliet','11/09/2021',4,'Please cancel 1 seat from my booking');
INSERT INTO BOOKING (CUSTOMER,PERFORMANCE,PERFORMANCE_DATE,BOOKED_BY,INSTRUCTION) values ('ruby.m5@gmail.com','Death of a Salesman','27/09/2021',2,'I want to add meals to my booking');
INSERT INTO BOOKING (CUSTOMER,PERFORMANCE,PERFORMANCE_DATE,BOOKED_BY,INSTRUCTION) values ('woodp88@yahoo.com','The Lion King','05/09/2021',3,'Can you please waitlist 4 seats?');
INSERT INTO BOOKING (CUSTOMER,PERFORMANCE,PERFORMANCE_DATE,BOOKED_BY,INSTRUCTION) values ('m.clark12@gmail.com','Disney''s Frozen','18/09/2021',2,'Please upgrade my seats to Box Seats');
INSERT INTO BOOKING (CUSTOMER,PERFORMANCE,PERFORMANCE_DATE,BOOKED_BY,INSTRUCTION) values ('jamie_ol@gmail.com','Julius Caesar','07/09/2021',1,'');

-- TOOLs or TRIGGERs --
-- switch agent name to booked_by for updates --
CREATE OR REPLACE FUNCTION get_booked_by(agent_name VARCHAR(100))
    RETURNS INTEGER AS $$
     DECLARE
    val INTEGER;
BEGIN
    SELECT AGENTID INTO val FROM AGENT WHERE username = agent_name LIMIT 1;
    IF val is NULL
        THEN RAISE EXCEPTION 'agent doesnt exists';
    END IF;
    return val;
END;
$$ LANGUAGE plpgsql;

commit;
"""
conn = openConnection()
cursor = conn.cursor()
cursor.execute(sql)
'''

# Delete this before running flask app


