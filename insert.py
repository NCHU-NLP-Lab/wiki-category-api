import os
import requests
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers


if __name__ == '__main__':

    ans = input(
        "Are you sure? document will be duplicated if you do that! Enter y to insure: ")
    if ans != "y" and ans != "Y":
        exit()

    input_path = r"extract.txt"

    load_dotenv()
    print(os.environ["ESURL"])

    try:
        # connect to Elasticsearch DB
        es = Elasticsearch(os.environ["ESURL"], connection_class=RequestsHttpConnection, use_ssl=True,
                           verify_certs=False, max_retries=5, retry_on_timeout=True, send_get_body_as='POST')
        requests.packages.urllib3.disable_warnings()

        i = 0
        actions = []
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                i += 1
                # print(line[:-1])
                category, entity = line[:-1].split("<->")
                # print(category, entity)
                actions.append({
                    "_index": "wiki-category2",
                    "_op_type": "index",
                    "_source": {
                        "category": category,
                        "entity": entity
                    }
                })

                if i % 1000 == 0:
                    print(f"insert {i} documents")
                    helpers.bulk(es, actions)
                    actions = []
                    # break

            if len(actions) != 0:
                helpers.bulk(es, actions)
                actions = []

            print("insert complete!")
            print("total line:", i)

    except Exception as e:
        print(e)
