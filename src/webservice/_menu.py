from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Menu(Base):
    __tablename__ = 'tbl_Menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    parent = db.Column(db.Integer, db.ForeignKey('tbl_Menu.id'))
    children = db.relationship("Menu")
    order = db.Column(db.Integer)
    level = db.Column(db.Integer)


    @staticmethod
    def get_all_menus():
        output = []
        root_menus = db.session.query(Menu).filter(Menu.parent == None)
        for root in root_menus:
            output.append({'id': root.id, 'name': root.name, 'display_name': root.name,
                           'parent': root.parent, 'parent_name': '', 'order': root.order})
            root.children = sorted(root.children, key=lambda structure: structure.order)
            for child in root.children:
                output.append({'id': child.id, 'name': child.name, 'display_name': '-> '+child.name,
                               'parent': child.parent, 'parent_name': root.name, 'order': child.order})
                child.children = sorted(child.children, key=lambda structure: structure.order)
                for grandchild in child.children:
                    output.append({'id': grandchild.id, 'name': grandchild.name, 'display_name': '-> -> '+grandchild.name,
                                   'parent': grandchild.parent, 'parent_name': child.name, 'order': grandchild.order})
        db.session.commit()
        return jsonify({'response': output})

    @staticmethod
    def create_new_menu(request):
        data = request.get_json()

        new_menu = Menu(name=data["name"], parent=data["parent"])
        db.session.add(new_menu)
        db.session.commit()
        return jsonify({'result': 'Menu has been created'})

    @staticmethod
    def update_menu(request):
        data = request.get_json()
        menu = db.session.query(Menu).filter_by(id=data['id']).first()
        if 'name' in data:
            menu.name = data['name']
        if 'parent' in data:
            menu.parent = data['parent']
        db.session.commit()
        return jsonify({'result': 'Menu has been changed'})

    @staticmethod
    def delete_menu(request):
        data = request.get_json()
        menus = db.session.query(Menu).filter(Menu.id.in_(data['id'])).all()
        for menu in menus:
            db.session.delete(menu)
        db.session.commit()

        return jsonify({'result': 'Menu has been deleted'})

    @staticmethod
    def get_menu_fields_menus():
        rows = db.session.query(Menu).all()
        output = []
        for row in rows:
            output.append({'id': row.id, 'name': row.name})
        db.session.close()
        return jsonify({'response': output})
