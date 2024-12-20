# endpoints.py
from flask import jsonify, request
from tables import User, Chanel
from database import Base, engine, metadata, init_db, get_db
from services import register_user, get_table_chanel, add_hashing_chanel, get_last_chanel

def configure_routes(app):
    @app.route('/inviteUser', methods=['POST'])
    def invite_user():
        data = request.json
        hash_admi = data['hash_admi']
        hash_guest = data['hash_guest']
        name_chanel = data['name_chanel']
        
        register_user(hash_admi)
        register_user(hash_guest)
        
        db = next(get_db())
        user1 = db.query(User).filter(User.hashing == hash_admi).first()
        user2 = db.query(User).filter(User.hashing == hash_guest).first()
        
        if not user1 or not user2:
            return jsonify({'message': 'Users not found', 'status': 404}), 404
            
        if getattr(user1, name_chanel) == 0:
            last_channel_id = get_last_chanel()
            print(f"last_channel_id : {last_channel_id}")
            setattr(user1, name_chanel, last_channel_id)
            db.commit()
            
        print("============================================")

        print(f"El canal de user2 es {getattr(user2, name_chanel)}")

        if getattr(user2, name_chanel) != 0:
            return jsonify({'message': 'Guest has the same channel', 'status': 400}), 400
            
        channel_number = getattr(user1, name_chanel)
        setattr(user2, name_chanel, channel_number)
        db.commit()

        print(f"El canal de user2 es {getattr(user2, name_chanel)}")

        add_hashing_chanel(channel_number, hash_guest)
        add_hashing_chanel(channel_number, hash_admi)
        
        return jsonify({'message': 'Users added to channel successfully', 'status': 200}), 200
    return app
