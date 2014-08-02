from flask import Blueprint, render_template, abort
from flask.ext.login import login_required
import speakeasy
from speakeasy.database import Page
from speakeasy.views.utils import menu

import datetime

pages = Blueprint('pages', __name__,
        template_folder='templates', url_prefix='/page')

print("Got pages.py")

@pages.route('/create', methods = ['GET'])
@login_required
def create_page():
    form = CreatePage()
    if form.validate_on_submit():
            if Page.query.filter_by(title=form.title.data).first() is None:
                new_page = Page( \
                        title=form.title.data, \
                        author_user_id=current_user.id, \
                        content=form.content.data, \
                        timestamp=datetime.datetime.now())
                db_session.add(new_page)
                db_session.commit()
                return render_template('index.html', user=current_user, menu=menu())
            else:
                flash('Could not create page, a page with that title already exists')
                return render_template('edit_page.html', form=form, menu=menu())

@pages.route('/edit/<id>', methods = ['GET'])
@login_required
def show_edit_page(id):
    form = CreatePage()
    page = Page.query.get(int(id))
    if page is None:
        abort(404)
    else:
        form.title.data = page.title
        form.content.data = page.content
        return render_template('edit_page.html', form=form, page_id=page.id, menu=menu(page.id))

@pages.route('/edit/<id>', methods= ['POST'])
@login_required
def edit_page(id):
    form = CreatePage()
    existing_page = Page.query.get(int(id))
    if existing_page is None:
        abort(404)
    else:
        existing_page.title=form.title.data
        existing_page.content = form.content.data
        db_session.add(existing_page)
        db_session.commit()
        flash("Page updated")
        return render_template('view_page.html',\
                page=existing_page,\
                title=existing_page.title,\
                menu=menu(existing_page.id),\
                user=current_user)

@pages.route('/create', methods = ['GET'])
@login_required
def show_create_page():
    form = CreatePage()
    return render_template('edit_page.html', form=form, menu=menu())

@pages.route('/<id>', methods = ['GET'])
def view_page(id):
    page = Page.query.get(int(id))
    if page is None:
        abort(404)
    else:
        return render_template('view_page.html', page=page, menu=menu(page.id), title=page.title)
