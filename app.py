from flask import Flask, render_template, jsonify, request
from checkers import Checkers

app = Flask(__name__)
game = Checkers()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.json
    from_pos = data['from']
    to_pos = data['to']
    board = data['board']

    # Update the game state with the current board
    game.set_board(board)

    # Attempt to make the move
    result = game.make_move(from_pos, to_pos)

    if result['valid']:
        return jsonify({
            'valid': True,
            'board': game.board,
            'currentPlayer': game.current_player
        })
    else:
        return jsonify({'valid': False, 'message': result['message']})


@app.route('/api/next', methods=['POST'])
def next():
    data = request.json
    board = data['board']
    player = data['currentPlayer']
    board, player = game.next(board, player)

    return jsonify({
        'valid': True,
        'board': board,
        'currentPlayer': player
    })

@app.route('/api/board')
def get_board():
    return game.board
    # return jsonify(game.get_board())


@app.route('/api/reset')
def reset_board():
    game.initialize_board()
    return game.board
    # return jsonify(game.get_board())

if __name__ == '__main__':
    app.run(debug=True)