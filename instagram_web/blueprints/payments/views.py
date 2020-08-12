from flask import Blueprint,render_template,redirect,url_for,flash, request
from werkzeug import secure_filename
from instagram_web.util.tokens import gateway
from models.payment import Payment
from models.user import User
from flask_login import current_user,login_required
import requests

payments_blueprint = Blueprint("payments",
                                __name__,
                                template_folder="templates")

@payments_blueprint.route("/new", methods=["GET"])
@login_required
def new(image_id):
    client_token= gateway.client_token.generate()
    print(client_token)
    return render_template("payments/new.html", client_token = client_token, image_id = image_id)

@payments_blueprint.route("/", methods=["POST"])
@login_required
def create(image_id):
    nonce_from_the_client = request.form["payment_method_nonce"]
    amount = request.form["amount"]

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
        "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        payment = Payment(user_id = current_user.id, image_id = image_id, amount = amount)
        payment.save()

        result = requests.post(
            "https://api.mailgun.net/v3/sandboxdb0c2cd1760a44d08240d1f87633eeab.mailgun.org/messages",
            auth=("api", "f{os.environ.get('MAILGUN_API_KEY')}"),
            data={"from": "Excited User <mailgun@sandboxdb0c2cd1760a44d08240d1f87633eeab.mailgun.org>",
                "to": ["afifjaz0202@gmail.com"],
                "subject": "Hello",
                "text": "Testing some Mailgun awesomeness!"})
        return redirect(url_for('images.show', id = image_id))

    else:
        flash("Failed to donate!", "danger")
        return redirect(url_for("payments.new", image_id = image_id))
