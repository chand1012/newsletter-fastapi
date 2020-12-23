import os
from deta import Deta

def set_subscriber(email, key, verified=False):
    deta = Deta(os.environ.get('DETA_PROJECT_KEY'))
    db = deta.Base("newsletter")
    db.put({'verified': verified, 'confirm_key':key}, email)

def get_subscriber(email):
    deta = Deta(os.environ.get('DETA_PROJECT_KEY'))
    db = deta.Base("newsletter")
    return db.get(email)

def query_subscriber(key):
    deta = Deta(os.environ.get('DETA_PROJECT_KEY'))
    db = deta.Base("newsletter")
    try:
        sub = next(db.fetch({'confirm_key': key}))[0]
    except IndexError:
        return None
    return sub

def get_subscribers(verified=True):
    deta = Deta(os.environ.get('DETA_PROJECT_KEY'))
    db = deta.Base("newsletter")
    subs_gen = db.fetch({'verified': verified}, pages=100, buffer=20)
    subs = []
    for sub_gen in subs_gen:
        subs += sub_gen
    return subs

def remove_sub(key):
    deta = Deta(os.environ.get('DETA_PROJECT_KEY'))
    db = deta.Base("newsletter")
    try:
        sub = next(db.fetch({'confirm_key': key}))[0]
    except IndexError:
        return False
    email = sub.get('key')
    return db.delete(email) is None

def remove_all_unverified():
    deta = Deta(os.environ.get('DETA_PROJECT_KEY'))
    db = deta.Base("newsletter")
    subs_gen = db.fetch({'verified': False}, pages=100, buffer=20)
    subs = []
    for sub_gen in subs_gen:
        subs += sub_gen
    for sub in subs:
        db.delete(sub.get('key'))
        
if __name__=='__main__':
    import random
    import string
    def random_string(N):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    fake_emails = ['d9Ep0gTgtWvW@example.com','zrycmIXjcWhD@example.com','YFoljG7LcPPT@example.com','0FX1KNCQOf0G@example.com','34vPHGlYnJPV@example.com','VY7KP9zyiX1a@example.com','7LdLo09MC205@example.com','9fOoiTojcohN@example.com','KPtgAJDgo7RL@example.com','inLLFNeE3pM9@example.com','nLSNhySU9ckF@example.com','7HAzJd0IcYnF@example.com','BxXtcq02Ttte@example.com','P4ab5yQmSDDA@example.com','REtiUK9kXSBQ@example.com','tG6enZGokk2I@example.com','CBZ1ftvoxWHo@example.com','yIABoO70vI8n@example.com','FwUrWA7qbQZF@example.com','8VrPHTo8vOVo@example.com','7zSdXyndRSuA@example.com','lvu8gEzD5dnL@example.com','OheOGfwPo7ZY@example.com','Ibx40MdD4OcL@example.com','gQ5ODsrD6nGu@example.com']
    for fake_mail in fake_emails:
        set_subscriber(fake_mail, random_string(47))

    subs = get_subscribers(False)
    print(subs)
    print(len(subs))

    fake_keys = []
    for sub in subs:
        fake_keys += [sub.get('confirm_key')]
    
    for fake_key in fake_keys:
        res = remove_sub(fake_key)
        if not res:
            print(f"Res is false for {fake_key}.")