import requests
from flask import Flask,render_template,request
from twilio.rest import Client

account_sid = 'take number from twilio'       #as twilio is showing security issues i has to replace this
auth_token = 'take from twilio'               #as twilio is showing security issues i has to replace this
client = Client(account_sid, auth_token)         #this allows to send msgs through phno

app = Flask(__name__, static_url_path='/static')    #app is obj that acts as interface btw web server and web pgs

@app.route('/')              #route is method helps to map with URLS
def registration_form():
    return render_template('login.html')   #it takes as 2 paramters (name of the pg which it has to render, parameters that takes as argument)

@app.route('/registration', methods=['GET','POST'])
def login_form():
    first_name = request.form['first_name']       #we are retriving data from login page & storing here as an obj
    last_name = request.form['last_name']
    email_id = request.form['email_id']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['id_proof']
    date = request.form['date']
    source_state = request.form['source_state']
    source_district = request.form['source_district']
    destination_state = request.form['dest_state']   #to confirm pass or not it depends on destination
    destination_district = request.form['destination_dt']

    full_name = first_name + "." + last_name

    r = requests.get('https://api.covid19india.org/v4/data.json')     #getting file; this link is giving covid related data in json format
    json_data = r.json()

    confirmed_cases = json_data[destination_state]['districts'][destination_district]['total']['confirmed']       #reading the file
    population = json_data[destination_state]['districts'][destination_district]['meta']['population']

    travel_pass = ((confirmed_cases / population) * 100)    #percentage

    if travel_pass < 30 and request.method == 'POST':
        status = 'Confirmed'
        client.messages.create(to="mynumber",    #as twilio is showing security issues i has to replace this
                               from_="+18285484149",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " + source_state + " to " +
                                    destination_state + " " + "Has " + " " + status + " On " + " " + ", Apply later")
        return render_template('registration.html', var=full_name,var1=email_id,var2=id_proof, var3=source_state, var4=source_district,
                        var5=destination_state, var6=destination_district, var7=phoneNumber,var8=date,var9=status)
    else:
        status = 'NOT CONFIRMED'
        client.messages.create(to="mynumber",
                               from_="+18285484149",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " +
                                    source_state + " to " + destination_state + " " + "Has " + " " + status + " On " + " " +
                                    ", Apply later")
        return render_template('registration.html',  var=full_name,var1=email_id,var2=id_proof, var3=source_state, var4=source_district,
                        var5=destination_state, var6=destination_district, var7=phoneNumber,var8=date,var9=status)

if __name__ == '__main__':
    app.run(port=9001, debug=True)
