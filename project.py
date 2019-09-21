from flask import Flask, request, render_template, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Users, Posts


app = Flask('__main__')


# connect to db
def connectDB():
    engine = create_engine('sqlite:///postApp.db')  
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    return session


# Mock Database
# users = [
#     {'name': 'Kevin kunis', 'user_id': '1', 'about': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Repudiandae, distinctio'},
#     {'name': 'Garnet Liew', 'user_id': '2', 'about': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Repudiandae, distinctio'},
# ]

# posts = [
#     {
#         'head': 'Intro Post',
#         'post': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias expedita delectus at iusto recusandae              voluptatem corporis consectetur ea veniam quaerat amet eveniet repellat perferendis optio, ipsam saepe            aperiam voluptas sed.',
#         'user_id': '1',
#         'post_id': '1',
#     },

#     {
#         'head': 'Hey this is my first post',
#         'post': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias expedita delectus at iusto recusandae              voluptatem corporis consectetur ea veniam quaerat amet eveniet repellat perferendis optio, ipsam saepe            aperiam voluptas sed.',
#         'user_id': '1',
#         'post_id': '2',
#     },

#     {
#         'head': 'First Post',
#         'post': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias expedita delectus at iusto recusandae              voluptatem corporis consectetur ea veniam quaerat amet eveniet repellat perferendis optio, ipsam saepe            aperiam voluptas sed.',
#         'user_id': '2',
#         'post_id': '3',
#     }
# ]

# Home Page
@app.route('/')
@app.route('/home')
def homePage():
    try:
        session = connectDB()
        posts = session.query(Posts).all()
        output = render_template('homePage.html', posts=posts) 
        return output
    except IOError as e:
        print(e)


# all users
@app.route('/users')
@app.route('/home/users')
def allUsers():
    session = connectDB()
    users = session.query(Users).all()
    output = render_template('allUsers.html', users=users, url_for=url_for)
    return output


# Profile page
@app.route('/<int:user_id>/profile')
@app.route('/home/<int:user_id>/profile')
def userProfile(user_id):
    session = connectDB()
    user_profile = session.query(Users).filter_by(user_id=user_id).one()
    posts = session.query(Posts).filter_by(user_id=user_id)
    output = render_template('userProfile.html', user=user_profile, posts=posts)
    return output


# Register page
@app.route('/register')
@app.route('/home/register', methods=['GET', 'POST'])
def registerPage():
    if request.method == 'POST':
        session = connectDB()
        newUser = Users(name=request.form['name'], about=request.form['about'])
        session.add(newUser)
        session.commit()
        return redirect(url_for('allUsers'))
    else:
        output = render_template('register.html', url_for=url_for)
        return output


# edit Profile
@app.route('/<int:user_id>/profile/edit', methods=['GET', 'POST'])
def editProfile(user_id):
    if request.method == 'POST':
        session = connectDB()
        user = session.query(Users).filter_by(user_id=user_id).one()
        if request.form['name'] != '':
            user.name = request.form['name']
        if request.form['about'] != '':
            user.about = request.form['about']
        session.add(user)
        session.commit()
        return redirect(url_for('userProfile', user_id=user_id))
    
    else:
        session = connectDB()
        user = session.query(Users).filter_by(user_id=user_id).one()
        output = render_template('editProfile.html', user=user, url_for=url_for)
        return output


# delete Profile
@app.route('/<int:user_id>/profile/delete', methods=['GET', 'POST'])
def deleteProfile(user_id):
    if request.method == 'POST':
        session = connectDB()
        user = session.query(Users).filter_by(user_id=user_id).one()
        if user.name == request.form['confirm']:    
            session.delete(user)
            session.commit()
            print('User {0} is deleted'.format(user.name))
            return redirect(url_for('allUsers'))
        else:
            print('The heading you typed is wrong..!!!')
    else:
        session = connectDB()
        user = session.query(Users).filter_by(user_id=user_id).one()
        output = render_template('deleteAcc.html', user=user, url_for=url_for)        
        return output


# add new post
@app.route('/<int:user_id>/profile/new-post', methods=['GET', 'POST'])
def addNewPost(user_id):
    if request.method == 'POST':
        session = connectDB()
        selected_user = session.query(Users).filter_by(user_id=user_id).one()
        newPost = Posts(head=request.form['heading'], post=request.form['main_post'], author=selected_user.name, user_id=user_id)
        session.add(newPost)
        session.commit()
        print('Added a post with post id - {0} by user {1}'.format(newPost.post_id, selected_user.name))
        return redirect(url_for('homePage'))
    else:
        session = connectDB()
        selected_user = session.query(Users).filter_by(user_id=user_id).one()
        output = render_template('newPost.html', user=selected_user, url_for=url_for)
        return output


# edit post
@app.route('/<int:user_id>/profile/<int:post_id>/edit', methods=['GET', 'POST'])
def editPost(user_id, post_id):
    if request.method == 'POST':
        session = connectDB()
        selected_post = session.query(Posts).filter_by(post_id=post_id).one()
        if request.form['heading'] != '':
            selected_post.head = request.form['heading']
        if request.form['main_post'] != '':
            selected_post.post = request.form['main_post']
        session.add(selected_post)
        session.commit()
        print('Edited post with post id - {0} by user {1}'.format(selected_post.post_id, user_id))
        return redirect(url_for('userProfile', user_id=user_id))
    else:
        session = connectDB()
        selected_post = session.query(Posts).filter_by(post_id=post_id).one()
        selected_user = session.query(Users).filter_by(user_id=user_id).one()    
        output = render_template('editPost.html', user=selected_user, post=selected_post, url_for=url_for)
        return output


# delete post
@app.route('/<int:user_id>/profile/<int:post_id>/delete', methods=['GET', 'POST'])
def deletePost(user_id, post_id):
    if request.method == 'POST':
        session = connectDB()
        selected_post = session.query(Posts).filter_by(post_id=post_id).one()
        if selected_post.head == request.form['confirm']:
            session.delete(selected_post)
            session.commit()
            print('Deleted post with id - {0} of user {1}'.format(post_id, user_id))
        return redirect(url_for('userProfile', user_id=user_id))
    else:
        session = connectDB()
        selected_post = session.query(Posts).filter_by(post_id=post_id).one()
        output = render_template('deletePost.html', post=selected_post, user_id=user_id, url_for=url_for)
        return output


@app.route('/<int:user_id>/profile/<int:post_id>/JSON')
def postJsonData(user_id, post_id):
    session = connectDB()
    user = session.query(Users).filter_by(user_id=user_id).one()
    post_id = session.query(Posts).filter_by(post_id=post_id).one()
    



# with app.test_request_context():
#     print(url_for('editPost', user_id='2', post_id='3'))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)