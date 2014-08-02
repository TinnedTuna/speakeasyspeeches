from flask import url_for, render_template, g
from flask.ext.login import current_user
from speakeasy.database import Page, User
from speakeasy import app, lm

def menu(active_id=None):
    pages = Page.query.order_by(Page.id)
    menu = []
    """

    for page in pages:
        menu_item = { 'menu_display' : page.title, \
                'menu_url' : url_for('view_page', id=page.id)}
        if active_id is not None:
            menu_item["active"] = active_id == page.id
        menu.append(menu_item)
    """
    contact_page = {
            'menu_display' : 'Contact',\
            'menu_url' : '/contact'}
            #'menu_url' : url_for('contact')}
    blog_page = {
            'menu_display' : 'Blog', \
            'menu_url' : '/blog'}
            #'menu_url' : url_for('show_blog')}
    if (active_id == len(menu) + 1):
        contact_page["active"] = True
    if (active_id == len(menu) + 2):
        blog_page["active"] = True
    menu.append(contact_page)
    menu.append(blog_page)
    return menu
                
def blog_menu_location():
    return len(Page.query.all()) + 2

@app.errorhandler(404)
def handle404(error):
    return render_template("404.html", menu=menu())

@app.errorhandler(401)
def handle401(error):
    return render_template("401.html", menu=menu())

@app.before_request
def before_request():
    if current_user is None:
        print "current_user is None"
    else:
        print "current_user is " + str(current_user)
    g.user = current_user

@lm.user_loader
def user_loader(id):
    return User.query.get(int(id))
