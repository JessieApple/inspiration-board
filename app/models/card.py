from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    board = db.relationship("Board", back_populates="cards")
    
    def to_dict(self):
        card_as_dict = {}
        card_as_dict["id"] = self.card_id
        card_as_dict["message"] = self.message
        card_as_dict["likes_count"] = self.likes_count
        if self.board_id:
            card_as_dict["board_id"] = self.board_id
        return card_as_dict
    
    @classmethod
    def from_dict(cls, card_info):
        new_card = cls(
            message = card_info["message"],
            likes_count = 0,
            board_id = card_info["board_id"]
        )

        return new_card