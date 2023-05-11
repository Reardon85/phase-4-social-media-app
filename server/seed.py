#!/usr/bin/env python3




from random import choice as rc, randint
from models import User, Post, Comment, Like, following
from faker import Faker
from config import app, db

fake = Faker()

bio_info = [
    "I'm a Funny Scientist",
    "I'm a Dumb Cat Lover",
    "I Don't Know How To Read!!! LULZ",
    "I Died 12 Years Ago and my Soul Got Stuck On This Site....",
    "I'm an Animal Lover who loves to Bike.",
    "I Use to Own an Airplane",
    "My Friends Call me Biz.",
    "I'm a very sad person.....",
    "Where did all the Cowboy's go?",
    "Does anyone Remember the movie the Matrix?",
    "I use to be a Professional Cowboy",
    "If you Follow me I'll Follow You Back!!!"
]

profile_pic = [
'https://the-tea.s3.us-east-2.amazonaws.com/profile1.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile10.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile11.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile12.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile13.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile14.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile15.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile16.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile18.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile17.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile19.jpeg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile2.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile20.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile21.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile22.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile23.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile24.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile25.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile26.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile27.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile29.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile28.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile3.webp',
'https://the-tea.s3.us-east-2.amazonaws.com/profile3.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile31.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile4.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile5.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile6.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile7.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile8.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/profile9.jpg'
]

content_list= [
    "Check out this Photo",
    "I took this when I was traveling",
    "This was so much fun",
    "You Know I'm gonna spill that tea",
    "Best day ever!",
    "I only wish that you guys could have seen it!",
    "Just living my best life!",
    "Feeling blessed and grateful today.",
    "Exploring new places and making memories.",
    "Sometimes the best therapy is a long drive and good music.",
    "Life is short, enjoy the little things.",
    "Creating moments that will last a lifetime.",
    "Happiness is a journey, not a destination.",
    "Life's too short to not take risks.",
    "Embracing the chaos and loving every minute of it.",
    "Dream big, work hard, stay focused, and surround yourself with good people.",
    "The only limit is the one you set for yourself.",
    "Always trust the journey, even if you don't understand it.",
    "Life is an adventure, embrace it with open arms.",
    "You are the artist of your own life, don't be afraid to paint outside the lines.",
    "Every day is a new opportunity to grow and learn.",
    "Make every moment count, and never forget to smile.",
    "Be the reason someone smiles today.",
    "Believe in yourself and all that you are.",
    "Chase your dreams and never look back.",
    "Love yourself, embrace your flaws, and never stop being you."
]

post_pic = [
'https://the-tea.s3.us-east-2.amazonaws.com/image1.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image1.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image11.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image12.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image2.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image3.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image4.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image5.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image6.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image7.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image8.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/image9.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img13.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img14.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img15.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img16.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img17.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img18.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img19.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img20.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img21.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img22.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img23.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img24.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img25.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img26.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img27.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img29.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img30.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img31.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img32.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img33.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img34.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img35.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img36.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img37.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img38.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img39.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img40.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img41.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img42.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img43.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img44.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img45.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img46.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img47.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img48.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img49.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img50.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img51.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img52.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img53.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img54.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img55.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img56.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img57.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img58.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img59.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img60.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img61.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img62.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img63.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img64.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img65.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img66.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img67.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img68.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img69.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img70.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img71.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img72.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img73.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img74.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img75.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img76.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img77.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img78.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img79.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img80.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img81.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img82.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img83.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img84.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img85.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img86.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img87.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img88.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img89.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img90.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img91.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img92.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img93.jpg',
'https://the-tea.s3.us-east-2.amazonaws.com/img94.jpg',
]


# 'https://the-tea.s3.us-east-2.amazonaws.com/emb1.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb2.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb3.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb4.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb5.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/emb6.png',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk1.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk10.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk11.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk12.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk13.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk14.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk15.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk16.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk17.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk19.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk2.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk21.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk22.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk23.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk24.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk25.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk26.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk27.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk28.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk29.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk3.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk30.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk31.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk32.webp'
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk33.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk4.jpg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk5.jpeg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk6.jpeg',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk7.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk8.webp',
# 'https://the-tea.s3.us-east-2.amazonaws.com/drunk9.jpg'


nice_comments = [
'So beautiful! 😍',
'Love this angle! 👌',
'This is giving me all the feels! ❤️',
'Wow, stunning photo! 📸',
"You're killing it, girl! 🔥",
'Goals! 💪',
'This looks like so much fun!',
'Where is this? I need to go there! 🌴',
'That made me smile! 😊',
'Obsessed with this look!',
'So jealous, wish I was there! 😩',
'Incredible shot! 🤩',
'You are a true inspiration! 💫',
'I need this in my life!',
'Can I borrow this image? 😉',
'This makes me want to book a flight ASAP! ✈️',
'Gorgeous as always! 💕',
'This is the definition of vacation goals! 🏖️',
"You're living your best life! 👏",
"I can't get enough of this picture!", 

]

bad_comments = [
"This is hilarious!",
"I can't stop laughing at this! 🤣",
"This made my day! 😆",
"I'm crying laughing! 😭",
"You always know how to make me laugh!",
"I needed this laugh, thank you!",
"How do you come up with this stuff?!", 
"You're too funny! 😂",
"I just snorted my drink!", 
"I can't breathe, this is too funny!",
"I'm sharing this with all my friends! 😂",
"You win the internet today! 🏆",
"This is the best thing I've seen all week!",
"My sides hurt from laughing so hard!",
"You're a comedic genius!",
"I'm going to be laughing about this all day!",
"This is the type of content I live for! 😂",
"You're officially my favorite Tea account!",
"I'm sending this to everyone I know!",
"You deserve an award for this post!",

]


with app.app_context():

    print('Deleting All Objects...')
    db.session.query(following).delete()


    Comment.query.delete()
    Like.query.delete()
    Post.query.delete()
    User.query.delete()
    db.session.commit()


    print('Creating User objects...')


    users = []
    posts = []

    for i in range(100):
        user = User(
            email=fake.email(),
            username=fake.name(),
            avatar_url=rc(profile_pic),
            bio= rc(bio_info)
        )
        user.password_hash = "flatiron"
        users.append(user)

    print('Making Each User follow 5 other Users')

    for user in users:
        for i in range(5):
            user.following.append(rc(users))


    print('Adding User objects to transaction...')
    db.session.add_all(users)
    print('Committing transaction...') 
    db.session.commit() 
    print('Complete.')

    print("Having Each User make 5 posts")
    for user in users:
        for i in range(5):
            post = Post(
                user_id = user.id,
                image=rc(post_pic),
                content=rc(content_list)
            )
            posts.append(post)

    print('Adding Post objects to transaction...')
    db.session.add_all(posts)
    print('Committing transaction...') 
    db.session.commit() 
    print('Complete.')

    print("Creating 5,000 randomly assigned Likes")
    # likes = []

    # super_users = User.query.limit(60).all()
    # super_posts = Post.query.limit(15).all()

    for i in range(10):

        post = posts.pop(1)
        index = randint(50, 99)
        for i in range(index):
            like = Like(user_id=users[i].id, post_id=post.id)
            db.session.add(like)


    # print(len(likes))
    # db.session.add_all(likes)
    # print('Committing transaction...') 
    # db.session.commit() 
    # print('Complete.')

    likes = []

    users_list = list(users)


    for user in users_list:
        posts_list = list(posts)
        print("Entering loop")

        for i in range(randint(1, 100)):
            print(i)
            random_index = randint(0, len(posts_list) - 1)
            post = posts_list.pop(random_index)
            like = Like(user_id=user.id, post_id=post.id)
            likes.append(like)
            db.session.add(like)

    # for user in users:

    #     if user.id == None:
    #         print('none')

    # for post in posts:

    #     if post.id == None:
    #         print('none')

    # for post in posts:
    #     print(post.id)





    # for i in range(5000):

    #     post_id = rc(posts).id
    #     user_id = rc(users).id
        
    #     like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
    #     if not like:
    #         new_like = Like(user_id=user_id, post_id=post_id)
    #         # likes.append(new_like)
    #         db.session.add(like)
    #         db.session.commit()


        # like = Like(
        #     user_id= rc(users).id,
        #     post_id= rc(posts).id
        # )


    print('Adding Like objects to transaction...')
    print(len(likes))
    # db.session.add_all(likes)
    print('Committing transaction...') 
    db.session.commit() 
    print('Complete.')

    print("Creating 1,000 randomly assigned comments ")

    comments = []

    for i in range(1000):
        comment = Comment(
            user_id= rc(users).id,
            post_id= rc(posts).id,
            content= rc(nice_comments)
        )
        comments.append(comment)
    
    print('Adding Comment objects to transaction...')
    db.session.add_all(comments)
    print('Committing transaction...') 
    db.session.commit() 
    print('Complete.')

    

