#Server
from flask import Flask, jsonify, request, abort
from employeeDAO import employeeDAO

app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)

#@app.route('/')
#def index():
#    return "Hello, World!"

#curl "http://127.0.0.1:5000/books"
@app.route('/employees')
def getAll():
    #print("in getall")
    results = employeeDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/books/2"
@app.route('/employees/<int:id>')
def findById(id):
    foundEmployee = employeeDAO.findByID(id)

    return jsonify(foundEmployee)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books
@app.route('/employees', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    employee = {
        "fname": request.json['fname'],
        "lname": request.json['lname'],
        "position": request.json['position'],
        "age": request.json['age'],
    }
    values =(employee['fname'],employee['lname'], employee['position'],employee['age'])
    newId = employeeDAO.create(values)
    employee['id'] = newId
    return jsonify(employee)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"author\":\"someone\",\"price\":123}" http://127.0.0.1:5000/books/1
@app.route('/employees/<int:id>', methods=['PUT'])
def update(id):
    foundEmployee = employeeDAO.findByID(id)
    if not foundEmployee:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'age' in reqJson and type(reqJson['age']) is not int:
        abort(400)

    if 'fname' in reqJson:
        foundEmployee['fname'] = reqJson['fname']
    if 'lname' in reqJson:
        foundEmployee['lname'] = reqJson['lname']
    if 'position' in reqJson:
        foundEmployee['position'] = reqJson['position']
    if 'age' in reqJson:
        foundEmployee['age'] = reqJson['age']
    values = (foundEmployee['fname'], foundEmployee['lname'], foundEmployee['position'],foundEmployee['age'],foundEmployee['id'])
    employeeDAO.update(values)
    return jsonify(foundEmployee)
        

    

@app.route('/employees/<int:id>' , methods=['DELETE'])
def delete(id):
    employeeDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)