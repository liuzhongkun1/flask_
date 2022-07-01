from flaskScript import db

class Users(db.Model):
    __tablename__ = "users"  # 设置表名
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))


