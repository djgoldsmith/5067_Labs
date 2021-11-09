import flask
import app

def handleRequest(request):
    if request.method == "GET":
        return flask.render_template('index.html')
    elif request.method == "POST":
        if not request.is_json:
            return "Invalid Request Body"
        
        theData = request.get_json()
        if "command" not in theData:
            return "Invalid Body Parameter"
        message = theData["command"]
        tripFilter, filtered = app.theFilter(message)
        if tripFilter:
            return filtered
        else:
            return app.execute(filtered)
        
    elif request.method == "OPTIONS":
        return '{"command": command to run}'
