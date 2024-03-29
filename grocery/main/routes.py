from flask import Blueprint, render_template, request
from grocery.models import User, Item

# similar to making an instance of a Flask object (see grocery/__init__.py) : additionally passing in the name of our 'Blueprint': mainappblueprint
mainappblueprint = Blueprint('mainappblueprint', __name__)


@mainappblueprint.route("/")
@mainappblueprint.route("/home")
def home():
    userstrue = User.query.filter_by(display_public=True).all()
    userstruelist_userids = []
    for i in userstrue:
        userstruelist_userids.append(i.id)
    page = request.args.get('page', 1, type=int)
    itemspaginated = Item.query.filter(Item.user_id.in_(userstruelist_userids)).paginate(page=page, per_page=3)
    items_public = Item.query.filter(Item.user_id.in_(userstruelist_userids))
    # items = Item.query.order_by(Item.user_id.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', items=itemspaginated, users_ids=userstruelist_userids, items_public=items_public, user_pics_used=[])

@mainappblueprint.route("/about")
def about():
    return render_template('about.html', title="About Page")