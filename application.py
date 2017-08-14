from flask import Flask, render_template, url_for, jsonify, request, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DbSession = sessionmaker(bind=engine)
session = DbSession()

# dummy variables

catalog = {'name' : 'Soccer'}






@app.route('/')
@app.route('/catalog/')
def showCategories():
	catalogs = session.query(Category).all()
	items = session.query(Item).order_by(Item.time.desc())
	return render_template('catalog.html', catalogs = catalogs, items = items)

@app.route('/catalog/<itemCategory>/items/')
def showItems(itemCategory):
	catalogs = session.query(Category).all()
	items = session.query(Item).filter_by(itemCategory=itemCategory).order_by(Item.time.desc())
	#return ("this page will show all the items for the itemCategory %s" % itemCategory)
	return render_template('specific_category.html', catalogs=catalogs, item_category=itemCategory,  items =items)

@app.route('/catalog/<itemCategory>/<item>/')
def showItemDescription(itemCategory, item):
	item = session.query(Item).filter_by(name=item).first()
	#return ("this page will show a short description of itemCategory %s and item %s" % (itemCategory, item))
	return	render_template("item_description.html", item = item)

@app.route('/catalog/<itemCategory>/<item>/edit/', methods=['GET', 'POST'])
def editItem(itemCategory, item):

	if request.method == 'POST':
		editedItem = session.query(Item).filter_by(name=item).one()
		return editedItem.name
	else:
		catalogs = session.query(Category).all()
		item = session.query(Item).filter_by(name=item).first()
		return render_template('edit_item.html', catalogs = catalogs , item = item, itemCategory = itemCategory)

@app.route('/catalog/<itemCategory>/<item>/delete')
def deleteItem(itemCategory, item):
	item = session.query(Item).filter_by(name=item).first()
	#return ("this page will contain template to delete item %s from itemCategory %s" % (item, itemCategory))
	return render_template('delete_item.html', itemCategory = itemCategory, item= item)

@app.route('/catalog.json/')
def catalogJSON():
    items = session.query(Item).all()
    return jsonify(Catalog=[i.serialize for i in items])


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)