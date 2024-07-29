import json
import os
import chromadb
from sentence_transformers import SentenceTransformer
import spacy


def process_query(query):
    #will take query string and return similar docs
    #convert to embeds
    model = SentenceTransformer("all-mpnet-base-v2")
    query_embed = model.encode([query])

    #extract tags
    nlp_ner = spacy.load("./outputs/model-best")
    tags = nlp_ner(query)
    temp = {}
    for ent in tags.ents:
        temp[str(ent.label_)] = str(ent.text)
    tags = temp

    #create a list of dicts to add filters to metadata
    filters = []

    if("COLOR" in tags):
        filters.append({
            "color" : tags["COLOR"]
        })

    if("UNDER_RATE" in tags):
        value = tags["UNDER_RATE"][6:]
        filters.append({
            "price" : {
                "$lte" : int(value)          #less than or equal to
            }
        })

    if("ABOVE_RATE" in tags):
        value = tags["ABOVE_RATE"][6:]
        filters.append({
            "price" : {
                "$gte" : int(value)          #greater than or equal to
            }
    })
        
    #get collection
    client = chromadb.PersistentClient(path = os.getcwd())
    collection = client.get_collection("clothes_data")

    #run query
    if(len(filters) == 0):
        #cant use and in this case
        sim_docs = collection.query(
        query_embeddings = query_embed,
        n_results = 10
    ) 
        
    elif(len(filters) == 1):
        sim_docs = collection.query(
        query_embeddings = query_embed,
        n_results = 10,
        where = filters[0]
    )  

    else:
        sim_docs = collection.query(
        query_embeddings = query_embed,
        n_results = 10,
        where={
            "$and" : filters
        }
    )  
        
    #now convert sim_docs tp list of dicts
    #each dict containing: product_name, price, photo_url
    return sim_docs["metadatas"][0]


def html_table(data):
    #take in a list of dicts, and outputs code for html table
    temp = """<table>
                <tr>
                    <th>Name</th>
                    <th>Image</th>
                    <th>Price</th>
                </tr>"""
    
    for ele in data:
        temp += f"""<tr>
                        <td>{ele["name"]}</td>
                        <td><img src = "{ele["img_url"]}"></img></td>
                        <td>{ele["price"]}</td>
                    </tr>"""
    
    temp += "</table>"
    return temp
        