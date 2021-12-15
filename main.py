import os
import requests
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, RequestsHttpConnection
from flask import Flask, request
import json
import datetime

app = Flask(__name__)

load_dotenv()

# connect to Elasticsearch DB
es = Elasticsearch(os.environ["ESURL"], connection_class=RequestsHttpConnection, use_ssl=True,
                   verify_certs=False, max_retries=5, retry_on_timeout=True, send_get_body_as='POST')
requests.packages.urllib3.disable_warnings()


@app.route("/")
def index():
    return "Server is ready!"


@app.route("/getCategory", methods=["GET"])
def getCategory():
    try:
        # get parameters
        entity = request.args.get("entity")
        size = request.args.get("size")
        from_ = request.args.get("from")

        # must have entity
        if entity == None:
            raise Exception("No entity!")
        # default size is 10
        if size == None:
            size = 10
        # default from is 0
        if from_ == None:
            from_ == 0

        # search from ES
        query = {
            "match": {
                "entity": entity
            }
        }
        res = es.search(index="wiki-category2", size=size,
                        from_=from_, query=query)

        return json.dumps(res["hits"], ensure_ascii=False)

    except Exception as e:
        # return error
        res = {
            "status": "fail",
            "data": f"{e}"
        }
        write_log(str(e))

        return json.dumps(res)


@app.route("/getEntity", methods=["GET"])
def getEntity():
    try:
        # get parameters
        category = request.args.get("category")
        size = request.args.get("size")
        from_ = request.args.get("from")

        # must have category
        if category == None:
            raise Exception("No category!")
        # default size is 10
        if size == None:
            size = 10
        # default from is 0
        if from_ == None:
            from_ == 0

        # search from ES
        query = {
            "match": {
                "category": category
            }
        }
        res = es.search(index="wiki-category2", size=size,
                        from_=from_, query=query)

        return json.dumps(res["hits"], ensure_ascii=False)

    except Exception as e:
        # return error
        res = {
            "status": "fail",
            "data": f"{e}"
        }
        write_log(str(e))

        return json.dumps(res)


def write_log(text):
    with open("log.txt", "a") as file:
        file.write(
            f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")


if __name__ == '__main__':
    print("API server start!")
    app.run(host="0.0.0.0", port=11014)
