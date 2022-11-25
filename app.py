from flask import Flask, request, send_file
import logging
import os
from posgres.postgres import PostgresApi
import yaml

import zipfile  

app = Flask(__name__)



yaml_file = open("config.yaml", encoding="utf-8")
config = yaml.load(yaml_file, Loader=yaml.FullLoader)


UPLOAD_FOLDER = config["UPLOAD_FOLDER"]
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

path = os.path.dirname(__file__)

@app.route('/')
def default():
    return ""

@app.route('/post', methods=["POST"])
def insert_new():
    for file_name in request.files:
        request.files[file_name].save(os.path.join(app.config["UPLOAD_FOLDER"], f'{file_name}.pdf'))
        
        postgres_obj.execute_query(f"INSERT INTO public.test(name) VALUES ('{file_name}')")
        
    return "added", 200


@app.route('/get/<wanted_ids>', methods=["Get"])
def get_list(wanted_ids):
    wanted_ids += ','
    ids = wanted_ids.split(',')
    peoples_data = postgres_obj.execute_query(f"SELECT * FROM public.test where name IN {tuple(ids)}")
    
    list_of_files = [f"{UPLOAD_FOLDER}/{file_name[0]}.pdf" for file_name in peoples_data]
    list_of_files = list(dict.fromkeys(list_of_files))
    
    with zipfile.ZipFile(f'{path}/reports/out.zip', 'w') as zipMe:        
        for file in list_of_files:
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
        
    return send_file(
        open(f'{path}/reports/out.zip', 'rb'),
        as_attachment=True,
        download_name='archive.zip'
    )


if __name__ == '__main__':
    postgres_obj = PostgresApi()
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    
    app.run(debug=True,host='0.0.0.0', port=3)