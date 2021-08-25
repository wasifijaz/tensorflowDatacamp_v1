'''
from flask import request
from flask.app import Flask
from flask_restx import Api, Resource, reqparse
#import mailroomTrackingWebScraping as ws

app = Flask(__tid__)
#trackingList = []

@app.route('/<tid>/<webtid>')
def access_param(tid,webtid):
    #trackingList.append(int(source))
    print(tid, webtid)
    return (tid, webtid)
    
if __tid__ == '__main__':
    app.run(debug = True)
'''

from flask import Flask
from flask_restx import Api, Resource, reqparse
import mailroomTrackingWebScraping as wc
import time

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('tid', help='Specify your tid')
parser.add_argument('webname', help='Specify your website')

@api.route('/trackingID/webName')
class TrackingParcel(Resource):
    @api.doc(parser=parser)
    def get(self):        
        args = parser.parse_args()
        tid = args['tid']
        webname = args['webname']
        t_list = [tid]
        if webname == 'Package Mapping':
            wc.Package_Mapping(t_list)
            time.sleep(5)
        if webname == 'Package Trackr':
            wc.Package_Trackr(t_list)
            time.sleep(5)
        return "This is " + tid + " website: " + webname
    
if __name__ == '__main__':
    app.run()