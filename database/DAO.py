from database.DB_connect import DBConnect
from model.customer import Customer
from model.edge import Edge
from model.genre import Genre
from model.track import Track


class DAO():

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(i.InvoiceDate) as date
                    from invoice i
                    order by i.InvoiceDate"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(c.Country) as country
                    from customer c 
                    order by c.Country"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(date1, date2, country):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.*
                   from customer c, \
                        invoice i
                   where c.CustomerId = i.CustomerId \
                     and i.InvoiceDate between %s and %s
                     and c.Country = %s
                   group by c.CustomerId
                   order by c.CustomerId  """

        cursor.execute(query, (date1, date2, country,))

        for row in cursor:
            results.append(Customer(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdgesUguali(date1, date2, country,idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select c1.idC as id1, c2.idC as id2, sum(c1.tot) as p1, sum(c2.tot) as p2
                    from (select c.CustomerId  as idC, a.ArtistId as idA, sum(i.Total) as tot
                    from artist a, album al, track t, invoiceline il, invoice i, customer c 
                    where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId and t.TrackId = il.TrackId 
                    and il.InvoiceId = i.InvoiceId and i.CustomerId = c.CustomerId 
                    and i.InvoiceDate between %s and %s
                    and c.Country = %s
                    group by c.CustomerId, a.ArtistId) c1, 
                    (select c.CustomerId  as idC, a.ArtistId as idA, sum(i.Total) as tot
                    from artist a, album al, track t, invoiceline il, invoice i, customer c 
                    where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId and t.TrackId = il.TrackId 
                    and il.InvoiceId = i.InvoiceId and i.CustomerId = c.CustomerId 
                    and i.InvoiceDate between %s and %s
                    and c.Country = %s
                    group by c.CustomerId, a.ArtistId) c2
                    where c1.idC != c2.idC and c1.idA = c2.idA 
                    group by c1.idC, c2.idC
                    having sum(c1.tot) = sum(c2.tot)"""

        cursor.execute(query, (date1, date2, country, date1, date2, country,))

        for row in cursor:
            result.append(Edge(idMap[row["id1"]],idMap[row["id2"]],row["p1"],row["p2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesDiversi(date1, date2, country,idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select c1.idC as id1, c2.idC as id2, sum(c1.tot) as p1, sum(c2.tot) as p2
                    from (select c.CustomerId  as idC, a.ArtistId as idA, sum(i.Total) as tot
                    from artist a, album al, track t, invoiceline il, invoice i, customer c 
                    where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId and t.TrackId = il.TrackId 
                    and il.InvoiceId = i.InvoiceId and i.CustomerId = c.CustomerId 
                    and i.InvoiceDate between %s and %s
                    and c.Country = %s
                    group by c.CustomerId, a.ArtistId) c1, 
                    (select c.CustomerId  as idC, a.ArtistId as idA, sum(i.Total) as tot
                    from artist a, album al, track t, invoiceline il, invoice i, customer c 
                    where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId and t.TrackId = il.TrackId 
                    and il.InvoiceId = i.InvoiceId and i.CustomerId = c.CustomerId 
                    and i.InvoiceDate between %s and %s
                    and c.Country = %s
                    group by c.CustomerId, a.ArtistId) c2
                    where c1.idC != c2.idC and c1.idA = c2.idA
                    group by c1.idC, c2.idC
                    having sum(c1.tot) < sum(c2.tot)"""

        cursor.execute(query, (date1, date2, country, date1, date2, country,))

        for row in cursor:
            result.append(Edge(idMap[row["id1"]],idMap[row["id2"]],row["p1"],row["p2"]))

        cursor.close()
        conn.close()
        return result