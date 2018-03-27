from app import db, Chat

def main():
    print('Initializing the database...')
    db.create_all()
    print('Seeding the db... ')
    Chat.query.delete()
    qc = Chat(sender='QuickChat', message='Welcome to QuickChat! Start typing and whatever. When you\'re done, kill me.')
    db.session.add(qc)
    db.session.commit()
    print('Done!')

if __name__ == '__main__':
    main()
