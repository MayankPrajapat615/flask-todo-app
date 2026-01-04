# from app import db

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(100), nullable = False)
#     status = db.Column(db.String(20), default = "Pending")

#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    status = db.Column(db.STring(20),default = "Pendinf")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)