#! /usr/bin/python
from flask import Flask,request, jsonify,abort
import json



#Receives the request
def get_request():
    try:
        longitude = float(request.form.get('longitude'))
        latitude = float(request.form.get('latitude'))
    except:
        #return error message when the request is invalid 
        abort(400)
    state = get_location(longitude,latitude)
    return jsonify(state)

#Check if the point exist in any state
def get_location(longitude,latitude):
    state = 'none'
    with open('states.json') as data:
        for line in data:
            location  = json.loads(line)
            if point_inside(longitude,latitude,location['border']):
                state = location['state']
    return state



#function to check if the request point is inside the given area
def point_inside(x,y,poly, include_edges=True):
    n = len(poly)
    inside = False 
    x1,y1= poly[0]
    for i in range(1,n+1):
        x2,y2 = poly[i%n]
        if y > min(y1,y2):
            if y<= max(y1,y2):
                if x <= max(x1,x2):
                    if y1 != y2:
                        xinters = (y-y1)*(x2-x1)
                    if x1 == x2 or x <= xinters:
                        inside = not inside
        x1,y1 = x2,y2
    return inside

app = Flask(__name__)
app.add_url_rule('/','location',get_request,methods=['POST'])


#app.add_url_rule('/', 'location', methods=["POST"])

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)



