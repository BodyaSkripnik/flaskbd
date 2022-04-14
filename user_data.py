import sqlite3
import os

def db_request(query):
    data_base = os.environ['db_name']#переменая среды
    con = sqlite3.connect(data_base)
    # con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    result = cur.fetchall()
    # result = [dict(i) for i in cur.fetchall]
    con.close()
    return result

def artist(name):
    query = f"""select DISTINCT
	                artist.artist_name, album.album_name, album.album_id
                FROM track_list
                JOIN artist on track_list.artist_id = artist.id_artist
                JOIN album on track_list.album_id = album.album_id
                WHERE artist.artist_name = '{name}'"""
    result = db_request(query)
    print(result,'1111111111111111111111')
    spisok = []
    for row in result:
        print(row[0])
        text = row[0]
        text1 = row[1]
        text2 = row[2]
        spisok.append([text,text1,text2])
        print(spisok)
        newlist = []
        for el in spisok:
            print(el[0],'hello')
            songs = {'artist_name':el[0],
                'album_name':el[1],
                'album_id':el[2]}
            newlist.append(songs)
    return newlist

def song(artist,name):
        data_base = os.environ['db_name']
        con = sqlite3.connect(data_base)
        cur = con.cursor()
        cur.execute(f"""SELECT artist.artist_name,album.album_name,album.album_year FROM track_list
                    JOIN album on track_list.album_id = album.album_id
					JOIN artist on track_list.artist_id = artist.id_artist
					JOIN song on track_list.song_id = song.song_id
                    WHERE song.song_name = '{name}' and artist.artist_name = '{artist}'""")
        spisok = []
        for row in cur.fetchall():
            text = row[0]
            text1 = row[1]
            text2 = row[2]
            spisok.append([text,text1,text2])
            newlist = []
            for el in spisok:
                print(el[0],'hello')
                songs = {'artist_name':el[0],
                    'album_name':el[1],
                    'album_year':el[2]}
                newlist.append(songs)
        return newlist

def album(artist, album):
        data_base = os.environ['db_name']
        con = sqlite3.connect(data_base)
        cur = con.cursor()
        cur.execute(f""" select DISTINCT
	                song.song_name,song.song_year
                    FROM track_list
                    JOIN album on track_list.album_id = album.album_id
					JOIN artist on track_list.artist_id = artist.id_artist
					JOIN song on track_list.song_id = song.song_id
                    WHERE album.album_name = '{album}' and artist.artist_name = '{artist}'""")
        spisok = []
        for row in cur.fetchall():
            text = row[0]
            text1= row[1]
            spisok.append([text,text1])
            newlist = []
            for el in spisok:
                print(el[0],'hello')
                songs = {'song_name':el[0],
                    'song_year':el[1]}
                newlist.append(songs)
        return newlist

def search(search_string):
    search_dict = {
        'artist': db_request(f""" SELECT artist.artist_name
            FROM artist
            WHERE artist.artist_name like '%{search_string}%' """),
        'album': db_request(f""" SELECT album.album_name
            FROM album
            WHERE album.album_name like '%{search_string}%' """),
        'song': db_request(f""" SELECT song.song_name
            FROM song
            WHERE song.song_name like '%{search_string}%' """)
        }
    # search_dict= {}
    # for table in ['artist','album','song']:
    #     search_dict.update({table:db_request
    #     (f"""SELECT * FROM "{table}" WHERE "{table}_name" like '%{search_string}%'""")})
    return search_dict

def delete_song(artist_name,song_name):
    data_base = os.environ['db_name']
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    cur.execute(f"""SELECT song.song_id FROM track_list
                    JOIN album on track_list.album_id = album.album_id
					JOIN artist on track_list.artist_id = artist.id_artist
					JOIN song on track_list.song_id = song.song_id
                    WHERE song.song_name = '{song_name}' and artist.artist_name = '{artist_name}'""")
    for i in cur.fetchall():
        song = int(i[0])
    cur.execute(f"""SELECT * FROM song where song_id == '{song}'""")
    cur.execute(f"""DELETE FROM song WHERE song_id ='{song}'""")
    con.commit()
    cur.execute(f"""DELETE FROM track_list WHERE song_id ='{song}'""")
    con.commit()

def add_song(artist_name,album_name,song_name):
    data_base = os.environ['db_name']
    con = sqlite3.connect(data_base)
    cur = con.cursor()
    cur.execute(f"""SELECT * FROM song""")
    for i in cur.fetchall():
        if i[0] == i[0]:
            newid = i[0] + 1
    cur.execute(f"""SELECT * FROM track_list""")
    for el in cur.fetchall():
        newsong_id = el[1] - el[1]
        newsong_id = newsong_id + newid
        if el[3] == el[3]:
            tracknum_new = el[3] + 1
    cur.execute(f"""SELECT * FROM album""")
    for album in cur.fetchall():
        if album[1] == album[1]:
            album_id = album[0]
    cur.execute(f"""SELECT * FROM artist""")
    for artist in cur.fetchall():
        if artist[1] == artist[1]:
            artist_id = artist[0]
    
    cur.execute(f"""INSERT INTO song (song_id,song_name,song_text,song_year,origin_lang) 
                    VALUES ('{newid}','{song_name}','','','en')""")
    con.commit()
    cur.execute(f"""INSERT INTO track_list (artist_id,song_id,album_id,track_num) 
                    VALUES ('{artist_id}','{newsong_id}','{album_id}','{tracknum_new}')""")
    con.commit()