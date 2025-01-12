from extensions import db

class User(db.Model):
    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    FullName = db.Column(db.String(100), nullable=True)
    Email = db.Column(db.String(100), nullable=True)
    IsActive = db.Column(db.Boolean, default=True)
    CreatedAt = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship with UserPermissions
    permissions = db.relationship('UserPermission', back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(UserID={self.UserID}, Username='{self.Username}')>"



class Path(db.Model):
    __tablename__ = 'Paths'

    PathID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Path = db.Column(db.String(255), unique=True, nullable=False)
    Description = db.Column(db.String(255), nullable=True)

    # Relationship with UserPermissions
    permissions = db.relationship('UserPermission', back_populates='path', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Path(PathID={self.PathID}, Path='{self.Path}')>"
    

class UserPermission(db.Model):
    __tablename__ = 'UserPermissions'

    PermissionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    PathID = db.Column(db.Integer, db.ForeignKey('Paths.PathID'), nullable=False)
    GrantedAt = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    user = db.relationship('User', back_populates='permissions')
    path = db.relationship('Path', back_populates='permissions')

    def __repr__(self):
        return f"<UserPermission(PermissionID={self.PermissionID}, UserID={self.UserID}, PathID={self.PathID})>"

