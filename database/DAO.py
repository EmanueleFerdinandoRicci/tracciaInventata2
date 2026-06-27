from database.DB_connect import DBConnect
from model.edge import Edge
from model.genre import Genre
from model.track import Track


class DAO():

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select g.*
                    from genre g"""

        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(genreId):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.*
                    from track t 
                    where t.GenreId = %s"""

        cursor.execute(query,(genreId,))

        for row in cursor:
            result.append(Track(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(genreId, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.id as id1, t2.id as id2, count(*) as peso 
                    from (select t.TrackId as id, p.PlaylistId as p 
                    from track t, playlisttrack p 
                    where t.GenreId = %s and t.TrackId = p.TrackId) t1,
                    (select t.TrackId as id, p.PlaylistId as p
                    from track t, playlisttrack p 
                    where t.GenreId = %s and t.TrackId = p.TrackId) t2
                    where t1.id > t2.id and t1.p = t2.p
                    group by t1.id, t2.id"""

        cursor.execute(query, (genreId,genreId,))

        for row in cursor:
            result.append(Edge(idMap[row["id1"]],idMap[row["id2"]],row["peso"]))

        cursor.close()
        conn.close()
        return result



