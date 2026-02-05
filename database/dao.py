from database.DB_connect import DBConnect
from model.artist import Artist
from model.connection import Connection

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    # DA RIMUOVERE
    @staticmethod
    def get_artists_with_min_albums(min_albums, artists_dictionary):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT al.artist_id, COUNT(*) AS cnt
                FROM album al
                GROUP BY al.artist_id
                HAVING COUNT(*) >= %s
                """
        cursor.execute(query, (min_albums,))
        for row in cursor:
            artist_id = row['artist_id']
            artist = artists_dictionary[artist_id]
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_edges_with_complex_query(artists_dictionary):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT al1.artist_id AS artist_id1, al2.artist_id AS artist_id2, COUNT(DISTINCT t1.genre_id) AS n_genres
                FROM album al1, track t1, album al2, track t2
                WHERE t1.album_id = al1.id 
                AND t2.album_id = al2.id
                AND t1.genre_id = t2.genre_id
                AND al1.artist_id <> al2.artist_id
                GROUP BY al1.artist_id, al2.artist_id;
                """
        cursor.execute(query)
        for row in cursor:
            artist_id1 = row['artist_id1']
            artist_id2 = row['artist_id2']
            artist1 = artists_dictionary[artist_id1]
            artist2 = artists_dictionary[artist_id2]
            n_genres = row['n_genres']
            result.append(Connection(artist1, artist2, n_genres))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artists_for_min_track_duration(min_duration_in_ms, artists_dictionary):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT al.artist_id
                FROM album al, track tr
                WHERE al.id = tr.id
                AND milliseconds > %s
                """
        cursor.execute(query, (min_duration_in_ms,))
        for row in cursor:
            artist_id = row['artist_id']
            artist = artists_dictionary[artist_id]
            result.append(artist)
        cursor.close()
        conn.close()
        return result
