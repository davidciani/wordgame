from wgweb import app
from flask import jsonify, render_template, request
from wordgame import findWords, loadWordlist
from operator import itemgetter

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/_findwords')
def findwords():
    hand = request.args.get('hand','', type=str)
    prefix = request.args.get('prefix','', type=str)
    suffix = request.args.get('suffix','', type=str)
    required = request.args.get('required','', type=str)
    
    app.logger.debug('Hand: %s, Prefix: %s, Suffix: %s, Required: %s',hand,prefix,suffix,required)

    if not hand:
        return jsonify({'errors':{
                'title':'Invalid Request',
                'detail':'Request must contain a \'hand\' arg'
                }})

    wordlist = loadWordlist(open('enable1.txt'))

    return jsonify({
            'words': sorted(findWords(hand,prefix,suffix,required,wordlist), key=itemgetter('score','length'), reverse=True)})
