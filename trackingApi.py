from flask import Flask
from flask_restx import Api, Resource, reqparse
from numpy import empty
from pandas.core.dtypes.missing import notnull
import mailroomTrackingWebScraping as wc
import time
from werkzeug.exceptions import BadRequest
import pandas as pd
from werkzeug.datastructures import FileStorage
import os

app = Flask(__name__)
api = Api(app, version='1.0', title='PACKAGE TRACKING API', description='Package tracking using webscrapping techniquues.')

trackingResult = pd.DataFrame()

parser = reqparse.RequestParser()
parser.add_argument('Tracking ID', help='Enter your Tracking ID (For multiple enteries use comma):')
parser.add_argument('Website Name', help='Specify your website:\n\t1. Package Mapping\n\t2. Package Trackr')

@api.route('/TrackingPackage_UsingTrackingID')
class TrackingParcel(Resource):
    @api.doc(parser=parser)
    def get(self):        
        args = parser.parse_args()
        tid = args['Tracking ID']
        if not tid:
            raise BadRequest('Tracking Number Missing!')
        else:
            webname = args['Website Name']
            trackingIds = tid.split(',')
            if webname == 'Package Mapping' or webname == '1':
                trackingResult = wc.Package_Mapping(trackingIds)
                time.sleep(5)
                return trackingResult.to_json(), 200
            elif webname == 'Package Trackr' or webname == '2':
                trackingResult = wc.Package_Trackr(trackingIds)
                time.sleep(5)
                return trackingResult.to_json(), 200
            else:
                raise BadRequest('Invalid Website Name!')


upload_parser = api.parser()
upload_parser.add_argument('Upload CSV File', location='files', type=FileStorage)
upload_parser.add_argument('Website Name', help='Specify your website:\n\t1. Package Mapping\n\t2. Package Trackr')

@api.route('/TrackingPackage_UsingCSV')
@api.expect(upload_parser)
class UploadFile(Resource):
    def post(self):
        args = upload_parser.parse_args()
        file = args.get('Upload CSV File')
        split_tup = os.path.splitext(file.filename)
        if split_tup[1] == '.csv':
            trackingIds = wc.readCSV(file)
            webname = upload_parser['Website Name']
            if webname == 'Package Mapping' or webname == '1':
                trackingResult = wc.Package_Mapping(trackingIds)
                time.sleep(5)
                return trackingResult.to_json(), 200
            elif webname == 'Package Trackr' or webname == '2':
                trackingResult = wc.Package_Trackr(trackingIds)
                time.sleep(5)
                return trackingResult.to_json(), 200
            else:
                raise BadRequest('Invalid Website Name!')
        else:
            raise BadRequest('Invalid File Format! Select CSV file.')

if __name__ == '__main__':
    app.run(debug=True)