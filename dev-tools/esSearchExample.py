# Created as an examples to practice indexing a set of urls using elasticsearch
# Author: Jeff Schloemer
# Date: 01/02/2023

from elasticsearch import Elasticsearch

# Setup Search
numberSearchResults = 3

try:
    # Connect to the Elasticsearch cluster
    es = Elasticsearch(hosts=['https://localhost:9200'], http_auth=('elastic', '-gduI5VLflBbyGt4ozD6'), verify_certs=False)

    print("Elastic Connected")
except:
    # Handle connectivity issues
    print("WARN - Error with Elastic Configuration")

# Check if the 'webpage' index exists
if es.indices.exists(index='webpage'):
    print("Search Index Available")

    # Practice Retrieval
    #res = es.get(index="webpage", id=1)
    #print(res['_source'])
    
    # Practice Search 0
    #resp = es.search(index="webpage", query={"match_all": {}})
    #print("Got %d Hits:" % resp['hits']['total']['value'])
    #for hit in resp['hits']['hits']:
    #    print("%(timestamp)s %(url)s: %(text)s" % hit["_source"])
    
    ## Practice Search 1 - Match
    query = "QB50 WOD"
    #results = es.search(index='webpage', query={'match': {'message': query}}, sort= [{'_score': {'order': 'desc'}}], size=numberSearchResults)
    results = es.search(index='webpage', query={'match': {'text': query}}, sort= [{'_score': {'order': 'desc'}}], size=numberSearchResults)
    #print(results)
    
    #Parse results
    names = [docu['_source']['url'] for docu in results['hits']['hits']]
    scores = [docu['_score'] for docu in results['hits']['hits']]
    i = 0
    for name in names:
        score = scores[i]
        text = "[" + name + "](" + name + ") and score " + str(score)
        print(text)
        i = i+1
    
    ## Practice Search 2 - Exact Match
    print("Exact Match only")
    
    # Take the user's parameters and put them into a Python
    # dictionary structured like an Elasticsearch query:
    query_body = {
        "match": {
            'text': {
                'query': query,
                'minimum_should_match': '100%'
            }
        }
    }
    
    results = es.search(index='webpage', query=query_body, sort= [{'_score': {'order': 'desc'}}], size=numberSearchResults)
    #print(results)
    
    #Parse results
    names = [docu['_source']['url'] for docu in results['hits']['hits']]
    scores = [docu['_score'] for docu in results['hits']['hits']]
    i = 0
    for name in names:
        score = scores[i]
        text = "[" + name + "](" + name + ") and score " + str(score)
        print(text)
        i = i+1
        
 ## Practice Search 3 - Fuzzy Match
    print("Fuzzy Matches")
    
    # Take the user's parameters and put them into a Python
    # dictionary structured like an Elasticsearch query:
    query_body2 = {
        "match": {
            'text': {
                'query': query,
                "fuzziness": "AUTO"
            }
        }
    }
    
    results = es.search(index='webpage', query=query_body, sort= [{'_score': {'order': 'desc'}}], size=numberSearchResults)
    #print(results)
    
    #Parse results
    names = [docu['_source']['url'] for docu in results['hits']['hits']]
    scores = [docu['_score'] for docu in results['hits']['hits']]
    i = 0
    for name in names:
        score = scores[i]
        text = "[" + name + "](" + name + ") and score " + str(score)
        print(text)
        i = i+1
        
 ## Practice Search 4 - Cascading
    print("Cascade Matches")
    query = "QB50 WOD"
    
    # Take the user's parameters and put them into a Python
    # dictionary structured like an Elasticsearch query:
    query_body1 = {
        "match": {
            'text': {
                'query': query,
                'minimum_should_match': '100%'
            }
        }
    }
    
    # query_body2 = {
    #     "match": {
    #         'text': {
    #             'query': query,
    #             "fuzziness": "AUTO"
    #         }
    #     }
    # }
    
    query_body2 = {
        "match": {
            'text': {
                'query': query,
            }
        }
    }
    
    results1 = es.search(index='webpage', query=query_body1, sort= [{'_score': {'order': 'desc'}}], size=numberSearchResults)
    #print(results)
    
    #Parse results
    names1 = [docu['_source']['url'] for docu in results1['hits']['hits']]
    scores1 = [docu['_score'] for docu in results1['hits']['hits']]
    i = 0
    for name in names1:
        score1 = scores1[i]
        text = "[" + name + "](" + name + ") and score " + str(score1) + " - Exact Match"
        print(text)
        i = i+1
    
    if (i<numberSearchResults):
        # Didn't get three exact matches
        results2 = es.search(index='webpage', query=query_body2, sort= [{'_score': {'order': 'desc'}}], size=numberSearchResults)
        
        #Parse results
        names2 = [docu['_source']['url'] for docu in results2['hits']['hits']]
        scores2 = [docu['_score'] for docu in results2['hits']['hits']]
        i = 0
        
        for name in names2:
            if (name in names1):
                # Skip duplicate results
                i = i + 1
            else:
                score2 = scores2[i]
                text = "[" + name + "](" + name + ") and score " + str(score2) + " - Partial Match"
                print(text)
                i = i+1
        