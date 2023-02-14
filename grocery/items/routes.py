from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from grocery import db
from grocery.models import Item
from grocery.items.forms import NewItem

# similar to making an instance of a Flask object (see grocery/__init__.py) : additionally passing in the name of our 'Blueprint': itemsappblueprint
itemsappblueprint = Blueprint('itemsappblueprint', __name__)

@itemsappblueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_item():
    form = NewItem()
    if form.validate_on_submit():
        post = Item(item_name=form.item_name.data, detail=form.detail.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your item has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('new_item.html', title="New Item", form=form, legend='New Item')

#Consider changing to entire list
@itemsappblueprint.route("/item/<int:item_id>")
def item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', item_name=item.item_name, item=item)

@itemsappblueprint.route("/item/<int:item_id>/update", methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.user != current_user:
        abort(403)
    form = NewItem()
    if form.validate_on_submit():
        item.item_name = form.item_name.data
        item.detail = form.detail.data
        db.session.commit()
        flash('Your item has been updated!', 'success')
        return redirect(url_for('item', item_id=item.id))
    elif request.method == 'GET':
        form.item_name.data = item.item_name
        form.detail.data = item.detail
    return render_template('new_item.html', title="Update Item", form=form, legend='Update Item')

@itemsappblueprint.route("/item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.user != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Your item has been deleted!', 'success')
    return redirect(url_for('home'))
