from flask import Flask, render_template, url_for
app = Flask(__name__)

store_items = [
    {
        'author': 'Peter Hackley',
        'title' : 'needed item',
        'detail' : 'brand, count, description',
        'date_added' : 'April 10, 2023',
    },
    {
        'author': 'Jane Doe',
        'title' : 'Needed Item 2',
        'detail' : 'Name Brand, x2',
        'date_added' : 'April 11, 2023',
    },
]


@app.route("/")
@app.route("/home")
def hello():
    return render_template('home.html', store_items=store_items)

@app.route("/about")
def about():
    return render_template('about.html', title="About Page")


if __name__ == '__main__':
    app.run(debug=True)