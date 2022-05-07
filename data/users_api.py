import flask
from flask import jsonify, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=(
                    'id',
                    'surname',
                    'name',
                    'age',
                    'position',
                    'speciality',
                    'address',
                    'email',
                    'modified_date'
                )) for item in users]
        }
    )


@blueprint.route('/api/users/<int:users_id>', methods=['GET'])
def get_one_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=(
                    'id',
                    'surname',
                    'name',
                    'age',
                    'position',
                    'speciality',
                    'address',
                    'email',
                    'modified_date',
                    'city_from'
                ))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def add_users():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 [
                    'id',
                    'surname',
                    'name',
                    'age',
                    'position',
                    'speciality',
                    'address',
                    'email',
                 ]):
        return jsonify({'error': 'Bad request'})
    elif db_sess.query(User).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    users = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def edit_users(users_id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if not db_sess.query(User).get(users_id):
        return jsonify({'error': 'Not found'})
    users = db_sess.query(User).get(users_id)
    for key in request.json:
        if key == 'surname':
            users.surname = request.json['surname']
        if key == 'name':
            users.name = request.json['name']
        if key == 'age':
            users.age = request.json['age']
        if key == 'position':
            users.position = request.json['position']
        if key == 'speciality':
            users.speciality = request.json['speciality']
        if key == 'address':
            users.address = request.json['address']
        if key == 'email':
            users.email = request.json['email']
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


