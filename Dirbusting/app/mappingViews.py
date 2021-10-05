"""
Views for the mapping task
"""

import flask

from .meta import app


from .models import *



@app.route("/products")
def products():
    """
    Single Page Application for Products
    """
    theItem = flask.request.args.get("item")
    if theItem:
        #We Do A Query for It
        itemQry = Item.query.filter_by(id=theItem).first()
        if itemQry is None:
            flask.abort(404, "No Such Item")
        
        return flask.render_template("showItem.html",
                                     item = itemQry)
    else:
        #flask.abort(404, "No Args Specified")
        #return "No such product"

        books = Item.query.filter_by(category="book")
        books.filter_by(hidden=False)
        
        return flask.render_template("allItems.html",
                                     books = books)
    
#def listItems(itemId = None, category=None, hidden=False):
    
    
