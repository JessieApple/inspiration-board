from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards",__name__,url_prefix="/boards")

# example_bp = Blueprint('example_bp', __name__)
@boards_bp.route("",methods=["POST"])
def create_board():
    request_body = request.get_json()
    try:
        new_board = Board(title=request_body["title"],
                        owner=request_body["owner"])
    except KeyError:
        abort(make_response({
            "details":"Invalid data"
        },400))
    
    db.session.add(new_board)
    db.session.commit()
    
    response_body = {
        "board":{
        "id":new_board.board_id,
        "title":new_board.title,
        "owner":new_board.owner 
        }
    }
    
    return make_response(response_body,201)
    
# View a list of all boards
@boards_bp.route("",methods=["GET"])
def check_all_boards():
    boards = Board.query.all()
    
    boards_response = []
    for board in boards:
        boards_response.append({
            "id":board.board_id,
            "title":board.title,
            "owner":board.owner 
        })
    return jsonify(boards_response)

# Select a board
@boards_bp.route("/<board_id>",methods=["GET"])
def get_one_board(board_id):
    board = validation_model(Board,board_id)
    cards = [card.to_dict() for card in board.cards]
    return {
        "board":{
            "id":board.board_id,
            "title":board.title,
            "owner":board.owner,
            "cards":cards
        }
    }    
    
# CRUD for cards
cards_bp = Blueprint("cards",__name__,url_prefix="/cards")

    
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