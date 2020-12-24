FORM = '''
    <form method="POST" action="/subscribe">
        <div class="form-group">
            <label for="email">Email address</label>
            <input type="email" name="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Enter email" />
            <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
'''

ALREADY = '''
    <div id="main" role="main" class="container">
        <h1>This email has already been subscribed.</h1>
    </div>
'''

CONFIRMATION = '''
    <div id="main" role="main" class="container">
        <h1>Please confirm your subscription.</h1>
        <div class="entry">
            Please check your email for confirmation.
        </div>
    </div>
'''

def confirm_string(email):
    return f'''
        <div id="main" role="main" class="container">
            <h1>{email} has successfully been subscribed.</h1>
        </div>
    '''