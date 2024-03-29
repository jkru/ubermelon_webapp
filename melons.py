from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined



@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    if 'isLogged' not in session:
        session['isLogged'] = "no"
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons, isLogged=session['isLogged'])

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon, isLogged = session['isLogged'])

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    def format_price(intprice):
        return "$%.2f"%intprice

    melon_info = {}
    total = 0

    if 'cart' not in session:
        session['cart'] = []
        session['isLogged'] = 'no'      

        
    else:
        melon_ids = session['cart']
        for i in range(len(melon_ids)):
            melon_object = model.get_melon_by_id(melon_ids[i])
            melon_name = model.get_melon_by_id(melon_ids[i]).common_name
            if melon_name in melon_info:
                melon_info[melon_name][0] += 1
                melon_info[melon_name][2] = melon_info[melon_name][0] * melon_object.price
                melon_info[melon_name][3] = (format_price(melon_info[melon_name][2]))

            else: 
                melon_info[melon_name] = []
                melon_info[melon_name].append(1)
                melon_info[melon_name].append(melon_object)
                #second append for total price
                melon_info[melon_name].append(melon_object.price)
                #makes the price have dollar signs
                melon_info[melon_name].append(format_price(melon_info[melon_name][2]))

        
        for melon_kind, melon_information in melon_info.iteritems():
                total += melon_information[2]
    
    total = format_price(total)

    return render_template("cart.html", melon_info=melon_info, total = total, isLogged=session['isLogged'])

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
    if 'cart' in session:
        session['cart'].append(id)
    else:
        session['cart'] = [id]
    flash ('Successfully added!')

    #return render_template("cart.html")
    return redirect(url_for('shopping_cart'))


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")
    customer = model.get_customer_by_email(email)
    if customer == None:
        flash("Customer does not exist.")
        return redirect(url_for('process_login'))
    elif (password != customer.password):
        flash("Wrong password.")
        return redirect(url_for('process_login'))

    else: 
        session['email'] = customer.email
        session['givenname'] = customer.givenname
        session['lastname'] = customer.surname
        session['isLogged'] = "yes"
#        return render_template("loggedin.html",first = session['givenname'], last = session['lastname'])
        return redirect(url_for('show_account'))

    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    return "Oops! This needs to be implemented"

@app.route("/account")
def show_account():
    return render_template("loggedin.html",first = session['givenname'], last = session['lastname'])



@app.route("/logout")
def log_out():
    session.clear()
    session['isLogged'] = "no"
    # session['cart'] = []
    
    return redirect(url_for("show_login"))


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
