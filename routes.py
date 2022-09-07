# Importing the frameworks

from flask import *
import database

user_details = {}                   # User details kept for us
session = {}
page = {}

# Initialise the application
app = Flask(__name__)
app.secret_key = 'aab12124d346928d14710610f'


#####################################################
##  INDEX
#####################################################

@app.route('/')
def index():
    # Check if the user is logged in
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['title'] = 'Sydney Entertainment & Theatres System'
    
    return redirect(url_for('list_booking'))

#####################################################
##  LOGIN
#####################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
    # Check if they are submitting details, or they are just logging in
    if (request.method == 'POST'):
        # submitting details
        
        login_return_data = check_login(request.form['id'], request.form['password'])

        # If it is null, saying they have incorrect details
        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect login info, please try again.")
            return redirect(url_for('login'))

        # If there was no error, log them in
        page['bar'] = True
        strtest = 'Welcome back, ' + login_return_data['firstname'] + ' ' + login_return_data['lastname']
        flash(strtest)
        session['logged_in'] = True

        # Store the user details for us to use throughout
        global user_details
        user_details = login_return_data
        return redirect(url_for('index'))

    elif (request.method == 'GET'):
        return(render_template('login.html', page=page))

#####################################################
##  LOGOUT
#####################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    page['bar'] = True
    flash('You have been logged out. See you soon!')
    return redirect(url_for('index'))

#####################################################
##  LIST BOOKING
#####################################################

@app.route('/list_booking', methods=['POST', 'GET'])
def list_booking():
    # Check if the user is logged in
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # The user is just viewing the page
    if (request.method == 'GET'):
        # First check if specific event
        booking_list = database.findBookingsBySalesAgent(user_details['agentid'])
        if (booking_list is None):
            booking_list = []
            flash("There are no bookings in our system for sales agent " + user_details['firstname'] + " " + user_details['lastname'])
            page['bar'] = False
        return render_template('booking_list.html', booking=booking_list, session=session, page=page)

    # Try to get from the database
    elif (request.method == 'POST'):
        search_term = request.form['search']
        if (search_term == ''):
            booking_list_find = database.findBookingsBySalesAgent(user_details['agentid'])
        else:    
            booking_list_find = database.findBookingsByCustomerAgentPerformance(search_term)
        if (booking_list_find is None):
            booking_list_find = []
            flash("Booking \'{}\' does not exist for user ".format(request.form['search']) + user_details['username'])
            page['bar'] = False
        return render_template('booking_list.html', booking=booking_list_find, session=session, page=page)

#####################################################
##  Add Booking
#####################################################

@app.route('/new_booking' , methods=['GET', 'POST'])
def new_booking():
    # Check if the user is logged in
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # If we're just looking at the 'new booking' page
    if(request.method == 'GET'):
        times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        return render_template('new_booking.html', user=user_details, times=times, session=session, page=page)

	# If we're adding a new booking
    print(request.form['customer'])
    print(request.form['performance'])
    print(request.form['performance_date'])
    print(request.form['booked_by'])
    print(request.form['instruction'])
    success = database.addBooking(request.form['customer'],
                                 request.form['performance'],
                                 request.form['performance_date'],
                                 request.form['booked_by'],
                                 request.form['instruction'])
    if(success == True):
        page['bar'] = True
        flash("Booking added!")
        return(redirect(url_for('index')))
    else:
        page['bar'] = False
        flash("There was an error adding a new booking.")
        return(redirect(url_for('new_booking')))

#####################################################
## Update Booking
#####################################################
@app.route('/update_booking', methods=['GET', 'POST'])
def update_booking():
    # Check if the user is logged in
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # Get the booking number
    booking_no = request.args.get('booking_no')

    # Get the booking details
    booking_results = get_booking(booking_no, user_details['agentid'])

    # If we're just looking at the 'update booking' page
    if (request.method == 'GET'):
        # If booking details cannot be retrieved
        if booking_results is None:
            booking_results = []
		    # Do not allow viewing if there is no booking to update
            page['bar'] = False
            flash("You do not have access to update that record!")
            return(redirect(url_for('index')))

	    # Otherwise, if booking details can be retrieved
        times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        return render_template('update_booking.html', bookingInfo=booking_results, user=user_details, times=times, session=session, page=page)

    # If we're updating a booking
    success = database.updateBooking(request.form['booking_no'],
                                request.form['performance'],
                                request.form['performance_date'],
                                request.form['booked_by'],
                                request.form['instruction'])
    if (success == True):
        page['bar'] = True
        flash("Booking record updated!")
        return(redirect(url_for('index')))
    else:
        page['bar'] = False
        flash("There was an error updating the booking.")
        return(redirect(url_for('index')))

def get_booking(booking_no, agentid):
    print('routes.getBooking')
    for booking in database.findBookingsBySalesAgent(agentid):
        if booking['booking_no'] == booking_no:
            return booking
    return None

def check_login(username, password):
    print('routes.check_login')
    userInfo = database.checkUserCredentials(username, password)

    if userInfo is None:
        return None
    else:
        tuples = {
            'agentid': userInfo[0],
            'username': userInfo[1],
            'firstname': userInfo[2],
            'lastname': userInfo[3],
            'password': userInfo[4],
        }
        return tuples
