import braintree
from app import app

gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id = app.config.get("BT_MERCHANT_ID"),
            public_key = app.config.get("BT_PUBLIC_KEY"),
            private_key = app.config.get("BT_PRIVATE_KEY")
        )
    )