from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from services.CasinoSingleton import CasinoSingleton

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app, resources={r"/*": {"origins": "*"}})
  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# ROUTES
'''
GET /jetons/<id>
'''
@app.route('/jetons/<string:user_id>', methods=['GET'])
def get_jeton(user_id):
  try:
    jeton = CasinoSingleton.get_jeton_by_user_id(user_id)
    factor = CasinoSingleton.get_jeton_factor()

    return jsonify({
        'success': True,
        'jeton_amount': jeton.jeton_amount,
        'user_id': jeton.user_id,
        'factor': factor
    }), 200

  except Exception as e:
    print('ERROR', e)
    abort(404)

'''
PATCH /payment/<paymentMethod>
'''
@app.route('/payment/<paymentmethod>', methods=['PATCH'])
def patch_pay(paymentmethod):
  try:
    body = request.get_json()
    user_id = body['user_id']
    success = CasinoSingleton.run_checkout(paymentmethod, body['user_id'], body['payAmount'])
    jeton = CasinoSingleton.get_jeton_by_user_id(user_id)

    if (not success):
      abort(422)

    return jsonify({
        'success': True,
        'jeton_amount': jeton.jeton_amount,
    }), 200

  except Exception as e:
    print('ERROR', e)
    abort(404)


'''
POST /jetons
'''
@app.route('/jetons', methods=['POST'])
def post_jeton():
  try:
    body = request.get_json()

    if not ('user_id' in body and 'jeton_amount' in body):
      abort(422)

    new_jeton = CasinoSingleton.post_jeton(body['user_id'], body['jeton_amount'])

    formatted_jeton = {
      'user_id': new_jeton.user_id,
      'jeton_amount': new_jeton.jeton_amount
    }

    return jsonify({
      'success': True,
      'new_jeton': formatted_jeton
    }), 200

  except Exception as e:
    print(e)
    abort(404)

'''
PATCH /jetons/<id>
'''
@app.route('/jetons/<string:user_id>', methods=['PATCH'])
def patch_jeton(user_id):
  try:
    body = request.get_json()

    if not ('jeton_amount' in body):
      abort(422)
    
    if (body['jeton_amount'] is None):
      abort(422)

    updated_jeton = CasinoSingleton.set_player_jeton(user_id, body['jeton_amount'])

    return jsonify({
      'success': True,
      'user_id': updated_jeton.user_id,
      'jeton_amount': updated_jeton.jeton_amount
    }), 200

  except Exception as e:
    print(e)
    abort(404)