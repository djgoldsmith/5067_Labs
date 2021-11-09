var express = require('express');
var nunjucks = require('nunjucks');
var fs=require('fs');

var app = express();

app.use(express.json());       // to support JSON-encoded bodies
app.use(express.urlencoded()); // to support URL-encoded bodies

//Configure Template Engine
nunjucks.configure('templates', { autoescape: true, express: app});

var errorPage = "{% extends 'base.html' %}" +
    "{% block content %}" +
    "<h2>Error</h2>" +
    "<div class='alert alert-danger' role='alert'>" +
    "ERROR:  WHO is not a King" +
    "</div>" +
    "{% endblock content %}";



app.get('/', function(req, res) {
    //res.send("Hello World RELOADED"); //Just Text
    //nunjucks.render('index.html'); //Do the Render
    res.render('index.html');  //Render Index with Nunjucks

});

app.post("/", function(req, res){
    /* Deal with Post Request */
    //console.log(req.body);
    var theKing = req.body.king;
    var name = req.body.name;
    var gifts = req.body.gift.split("\n");

    var message = {"message": {"king": theKing,
			       "name": name,
			       "gifts": gifts}};

    //Filter
    var filterList = ["require", "child-process","exec"]
    for (var i=0; i<filterList.length; i++){
	theKing = theKing.replace(filterList[i], "");
	name = name.replace(filterList[i],"");
    }
    
    //Do our error checking
    if  (["Balthazar", "Melichor", "Gaspar"].includes(theKing)){
	res.render('index.html', message);  //Render Index with Nunjucks
    }
    else{
	//Replace string and render template
	var template = errorPage.replace("WHO", theKing);
	//Render
	var rendered = nunjucks.renderString(str = template, message);
	res.send(rendered);
    }
});

app.get("/debug", function(req,res){
    fs.readFile("server.js", 'utf-8', function(err, data){
	if (err) {
	    console.log("FILE READ ERROR");
	    console.log(err);
	}
	if (data) {
	    res.set('Content-Type', 'text/plain')
	    res.send(data);
	}
	//res.send(data);
    });
    //var reader = new FileReader("server.js");
    //res.send("DEBUG");
});

app.listen(3000);
console.log("Listening on port 3000...");

/*
@app.route('/debug')
def debug():
    return flask.Response(open(__file__).read(), mimetype='text/plain')
*/
