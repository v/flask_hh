from flask import Flask, render_template, request, redirect
import string, random

app = Flask(__name__)

def random_string():
    length = 6
    rv = ""

    for i in range(length):
        rv += random.choice(string.ascii_uppercase)

    return rv


@app.route('/')
def home():
    if 'url' in request.args:
        url = request.args['url']

        shortened_url_code = random_string()

        with open('urls', 'a') as handle:
            handle.write(url+'|'+shortened_url_code+"\n")

            handle.close()

        shortened_url = 'http://localhost:5000/short?code='+shortened_url_code

        return 'I received '+url+' as input. Here is your shortened URL '+shortened_url
    else:
        return render_template('index.html')

@app.route('/short')
def short():
    if 'code' in request.args:
        code = request.args['code']

        with open('urls') as handle:
            for line in handle.readlines():
                long_url, short = line.strip().split('|')

                if short == code:
                    return redirect(long_url)
        return 'Your code was not found'


    else:
        return 'Bad request'


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
