from neo4j import GraphDatabase


# Os dados foram importados seguindo o guide que surge quando se executa
# $ :play listings

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "listings"))


# 1 - Listar reviews e timestamp das mesmas de um dado utilizador
def get_reviews_from(tx, name):
    query = "match (u:User {name: \"%s\"}  )-[:WROTE]->(r:Review) RETURN u,r" % name
    print(query)
    
    for review in tx.run(query): 
        print(review["r"]["date"], review["r"]["comments"], sep=" - ")


# 2 - Ir buscar todas as listagens de um dado bairro com um preço inferior a price
def get_listings_in(tx, neighborhood, price):
    query = "match (l:Listing)-[n:IN_NEIGHBORHOOD]->(neigh:Neighborhood { name: \"%s\"}) where l.price < %d return l, neigh;" % (neighborhood, price)
    print(query)
    
    for record in tx.run(query): 
        print(record["l"]["name"], record["l"]["listing_id"])


# 3 - Listar os bairros com maior número de listagens, limitados por limit
def get_pop_neighborhoods(tx, limit):
    query = """ match (l:Listing)-[r:IN_NEIGHBORHOOD]->(n:Neighborhood)
                with count(r) as num_listings, n
                return n, num_listings
                order by num_listings desc
                limit %d;
            """ % limit
    print(query)

    for record in tx.run(query): 
        print("Neighborhood ID: " + record["n"]["neighborhood_id"], "Number of listings: " + str(record["num_listings"]), sep=" | ")


# 4 - Listar os hóspedes com mais que x listagens
def get_hosts_by_num_listings(tx, min_listings):
    query = """ match (h:Host)-[r:HOSTS]->(l:Listing)
                with count(r) as lists_hosted, h
                where lists_hosted > %d
                return h, lists_hosted
                order by lists_hosted desc
            """ % min_listings
    print(query)

    for record in tx.run(query): 
        print(record["h"]["name"], record["lists_hosted"], sep="\t| ")


# 5 - Ir buscar as x Amenity mais reviewed/popular
def get_pop_amenity(tx, x):
    query = """ match (rev:Review)-[r]->(l:Listing)
                match (l)-[has:HAS]->(a:Amenity)
                with count(r) as num_rev, a
                return a, num_rev
                order by num_rev desc
                limit %d;
            """ % x
    print(query)
  
    for record in tx.run(query):
        print(record["a"]["name"])


# Average reviews per listing for each host


# 6 - Média de reviews por cada listagem de cada host
def get_avg_rev(tx):
    query = """ match (h:Host)-[r:HOSTS]->(l:Listing)
            match (review:Review)-[rev:REVIEWS]->(l)
            with count(rev) as total_rev, h
            with avg(total_rev) as avg_rev, h
            return h, avg_rev
            order by avg_rev desc
            limit 15;
        """
    print(query)

    for record in tx.run(query):
        print(record["h"]["name"], record["avg_rev"])


# 7 - Obter o caminho mais curto entre um utilizador e um bairro
def get_shortest_path_user_neighborhood(tx, username, neighborhood):
    query = """ 
                match (u:User { name:\"%s\" }), (n:Neighborhood { name:\"%s\"}), p = shortestPath((u)-[*..4]-(n))
                return p
                order by length(p)
                limit 1
            """ % (username, neighborhood)
    print(query)

    for record in tx.run(query): 
        print('(', record["p"].start_node["name"], record["p"].start_node.id, ')',
        '-', len(record["p"]), '->',
        '(', record["p"].end_node["name"], record["p"].end_node.id, ')')


# 8 - Hosts que têm y amenity em todas as suas listagens e receberam mais de x reviews no total
def get_hosts_by_amen_and_pop(tx, amenity, no_rev):
    query = """ match (h:Host)-[r:HOSTS]->(l:Listing)
                match (rev:Review)-[review:REVIEWS]->(l)
                match (l)-[am:HAS]->(a:Amenity {name:"%s"})
                with count(rev) as no_reviews, h
                where no_reviews > %d
                return h, no_reviews
                order by no_reviews desc;
            """ % (amenity, no_rev)
    print(query)

    for record in tx.run(query):
        print("Host Name:", record["h"]["name"], "\t| Host ID:", record["h"]["host_id"])

    
# 9 - Média de listagens por host
def get_avg_listings(tx):
    query = """ match (n:Host)-[r:HOSTS]->(l:Listing)
                with count(r) as num_l, count(distinct n) as hosts
                with num_l * 1.0 / hosts as res
                return res;
            """
    print(query)

    for record in tx.run(query):
        print(record["res"])

# 10 - Hosts ordenados por total de reviews
def get_pop_hosts(tx, limit):
    query = """ match (h:Host)-[r:HOSTS]->(l:Listing)
                match (rev:Review)-[review:REVIEWS]->(l)
                with count(rev) as total_reviews, h
                return h, total_reviews
                order by total_reviews desc
                limit %d;
            """ % limit
    print(query)

    for record in tx.run(query):
        print(record["h"]["name"], ':', record["total_reviews"])


with driver.session() as session:

    print("## 1")

    ## 1
    session.read_transaction(get_reviews_from, 'William')

    print("\n## 2")

    ## 2
    session.read_transaction(get_listings_in, "East Riverside", 100)

    print("\n## 3")

    ## 3
    session.read_transaction(get_pop_neighborhoods, 15)

    print("\n## 4")

    ## 4
    session.read_transaction(get_hosts_by_num_listings, 20)

    print("\n## 5")

    ## 5
    session.read_transaction(get_pop_amenity, 10)

    print("\n## 6")

    ## 6
    session.read_transaction(get_avg_rev)

    print("\n## 7")

    ## 7
    session.read_transaction(get_shortest_path_user_neighborhood,"Jolie", "Hancock")

    print("\n## 8")

    ## 8
    session.read_transaction(get_hosts_by_amen_and_pop, "Gym", 10)

    print("\n## 9")

    ## 9
    session.read_transaction(get_avg_listings)

    print("\n## 10")

    ## 10
    session.read_transaction(get_pop_hosts, 15)  

    # Bom Natal Stor


driver.close()

