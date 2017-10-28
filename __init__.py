from flask import Flask, render_template
from flask import url_for, jsonify, request, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
from functools import wraps
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('postgresql://catalog:serginho@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('/var/www/FlaskApp/catalogUdacity/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('/var/www/FlaskApp/catalogUdacity/fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data.get('name')
    login_session['email'] = data.get('email')
    login_session['facebook_id'] = data.get('id')

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    login_session.clear()
    flash('you have been logged out')
    return redirect(url_for('showCategories'))

# Function decorator that controls user permissions
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            flash('Please log in to manage items.')
            return redirect(url_for('showCategories'))
        return func(*args, **kwargs)
    return decorated_function

"""
def user_is_owner(func):
    # Function decorator that controls user can edit
    @wraps(func)
    def decorated_function(*args, **kwargs):
        item_owner = session.query(Item.user_id).filter_by(name=item).first()
        email = login_session['email']
        current_user_id = getUserID(email)
        if item_owner != current_user_id or current_user_id is None:
            flash('you are not the owner of this product. Can not edit nor delete')
            return redirect(url_for('showCategories'))
        return func(*args, **kwargs)
    return decorated_function
"""


# JSON APIs to view Items Information
@app.route('/catalog/json/')
def catalog_as_json():
    items = session.query(Item).order_by(Item.time.desc())
    return jsonify(items=[r.serialize for r in items])


@app.route('/catalog/<itemCategory>/items/json/')
def one_catalog_as_json(itemCategory):
    items = session.query(Item).filter_by(itemCategory=itemCategory).order_by(Item.time.desc())
    return jsonify(catagory_items=[r.serialize for r in items])


@app.route('/')
@app.route('/catalog/')
def showCategories():
    catalogs = session.query(Category).all()
    items = session.query(Item).order_by(Item.time.desc())
    return render_template('catalog.html', catalogs=catalogs, items=items, login_session=login_session)


@app.route('/catalog/<itemCategory>/items/')
def showItems(itemCategory):
    catalogs = session.query(Category).all()
    items = session.query(Item).filter_by(itemCategory=itemCategory).order_by(Item.time.desc())
    # return ("this page will show all the items for the itemCategory %s" % itemCategory)
    return render_template('specific_category.html', catalogs=catalogs, item_category=itemCategory,
                            items=items, login_session=login_session)


@app.route('/catalog/<itemCategory>/<item>/')
def showItemDescription(itemCategory, item):
    item = session.query(Item).filter_by(name=item).first()
    # return ("this page will show a short description of itemCategory %s and item %s" % (itemCategory, item))
    return render_template("item_description.html", item=item, login_session=login_session)


@app.route('/catalog/<itemCategory>/item/add/', methods=['GET', 'POST'])
@login_required
def add_item(itemCategory):
    item_obj = session.query(Item).filter_by(itemCategory=itemCategory).first()
    if item_obj:
        if request.method == 'POST':
            name = request.form['new_name']
            description = request.form['new_description']
            category = item_obj.itemCategory
            email = login_session['email']
            current_user_id = getUserID(email)
            # return ("name:%s - description:%s - category:%s" % (name, description, category))
            if name and description:
                new_item_obj = Item(name=name, description=description,
                                    itemCategory=category, user_id=current_user_id)
                session.add(new_item_obj)
                session.commit()
                flash("item Added Successfully")
                return redirect(url_for('showCategories'))
            else:
                flash("need to include title and description!")
                return render_template('add_item.html', item_obj=item_obj, login_session=login_session,
                                        name=name, description=description)
        else:
            return render_template('add_item.html', item_obj=item_obj, login_session=login_session)
    else:
        return ("category %s does not exists" % itemCategory)


@app.route('/catalog/<itemCategory>/<item>/edit/', methods=['GET', 'POST'])
@login_required
def editItem(itemCategory, item):
    item_obj = session.query(Item).filter_by(name=item).first()
    if item_obj:
        email = login_session['email']
        current_user_id = getUserID(email)
        # print(item_obj.user_id)
        # print(current_user_id)
        if item_obj.user_id == current_user_id:
            if request.method == 'POST':
                new_name = request.form['new_name']
                new_description = request.form['new_description']
                new_category = request.form['new_category']
                if new_category and new_name and new_description:
                    item_obj.name = new_name
                    item_obj.description = new_description
                    item_obj.itemCategory = new_category
                    session.add(item_obj)
                    session.commit()
                    flash("Item succesfully edited!")
                    return redirect(url_for('showItems', itemCategory=new_category))
                else:
                    flash("include  new name, description and category!")
                    return redirect(url_for('editItem', itemCategory=itemCategory, item=item))
            else:
                catalogs = session.query(Category).all()
                return render_template('edit_item.html', catalogs=catalogs , item=item_obj,
                                        itemCategory=itemCategory, login_session=login_session)
        else:
            flash("you are not the owner of the item, can not edit nor delete")
            return redirect(url_for('showItems', itemCategory=itemCategory))
    else:
        return ("item %s does not exists" % item)


@app.route('/catalog/<itemCategory>/<item>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(itemCategory, item):
    item_obj = session.query(Item).filter_by(name=item).first()
    if item_obj:
        email = login_session['email']
        current_user_id = getUserID(email)
        # print(item_obj.user_id)
        # print(current_user_id)
        if item_obj.user_id == current_user_id:
            if request.method == 'POST':
                session.delete(item_obj)
                session.commit()
                flash("item %s deleted" % item_obj.name)
                return redirect(url_for('showItems', itemCategory=itemCategory))
            else:
                return render_template('delete_item.html', itemCategory=itemCategory,
                                        item=item, login_session=login_session)
        else:
            flash("you are not the owner of the item, can not edit nor delete")
            return redirect(url_for('showItems', itemCategory=itemCategory))
    else:
        return ("item %s does not exists!" % item)

@app.route('/catalog.json/')
def catalogJSON():
    items = session.query(Item).all()
    return jsonify(Catalog=[i.serialize for i in items])

app.secret_key = 'blabla2r24rwger3536tfsdr2345'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
