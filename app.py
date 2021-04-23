import os
import stripe

from flask import Flask, request, render_template, jsonify

stripe.api_key = 'sk_test_51IjAIUIeeZdHJeTnjIJSqlmQq5SFLelYE00VsTqOSS0NKEtLYuNy6Ei7ZHhZZerExPbvejJ6vhgjFPRsxQT8gRcQ00IUR7O86x'

app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "public"))


# Home route
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
  # Just hardcoding amounts here to avoid using a database
  item = request.args.get('item')
  title = None
  amount = None
  error = None

  if item == '1':
    title = 'The Art of Doing Science and Engineering'
    amount = 2300
  elif item == '2':
    title = 'The Making of Prince of Persia: Journals 1985-1993'
    amount = 2500
  elif item == '3':
    title = 'Working in Public: The Making and Maintenance of Open Source'
    amount = 2800
  else:
    # Included in layout view, feel free to assign error
    error = 'No item selected'

  return render_template('checkout.html', title=title, amount=amount, error=error)

# Success route
@app.route('/success', methods=['GET'])
def success():
  return render_template('success.html')


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 2000,
                        'product_data': {
                            'name': 'Stubborn Attachments',
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:5000' + '/success.html',
            cancel_url='http://localhost:5000' + '/cancel.html',
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403


if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)

