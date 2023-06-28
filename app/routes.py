from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards",__name__,url_prefix="/boards")

@boards_bp.route("",methods=["POST"])
def create_board():
    request_body = request.get_json()
    try:
        new_board = Board(
            title=request_body["title"],
            owner=request_body["owner"])
    except KeyError:
        abort(make_response({
            "details":"Invalid data"
        },400))
    
    db.session.add(new_board)
    db.session.commit()

    return {"board": new_board.to_dict()}, 201
    
# View a list of all boards
@boards_bp.route("",methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    
    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())

    return jsonify(boards_response)

# Select a board
@boards_bp.route("/<board_id>",methods=["GET"])
def get_one_board(board_id):
    board = validation_model(Board,board_id)

    return {"board":{board.to_dict()}}, 200

@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validation_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return {'details': f'Board {board.board_id} successfully deleted'}, 200

    
# CRUD for cards
cards_bp = Blueprint("cards",__name__,url_prefix="/cards")

@cards_bp.route("", methods=["POST"])
def add_card():
    request_body = request.get_json()
    try:
        message = request_body["message"]
        if len(message) <= 40:
            new_card = Card.from_dict(request_body)
        else:
            return {"details": "Message too long"}
    except KeyError:
        return {
            "details" : "Invalid data"
        }, 400
    
    db.session.add(new_card)
    db.session.commit()
    
    return {"card": new_card.to_dict()}, 201

@cards_bp.route("/<board_id>", methods=["GET"])
def get_all_cards_by_board(board_id):
    cards = Card.query.all()

    cards_response = []

    for card in cards:
        if card.board_id == int(board_id):
            cards_response.append(card.to_dict())

    return (jsonify(cards_response), 200)

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validation_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return {'details': f'Card {card.card_id} successfully deleted'}, 200


# Validation felper function
def validation_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"},400))
    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({
            "message":f"{cls.__name__} {model_id} not found"
        },404))
        
    return model 