GET_TAYANGAN_TERBAIK = """
  SELECT *
  FROM (
    SELECT F.id_tayangan, COALESCE(COUNT(start_date_time),0) AS total_view, \'film\' AS jenis
    FROM FILM F 
    LEFT OUTER JOIN (
      SELECT RN.id_tayangan, start_date_time, end_date_time
      FROM RIWAYAT_NONTON RN
      JOIN FILM F2 ON F2.id_tayangan = RN.id_tayangan
      WHERE 
        EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * F2.durasi_film * 60
        AND EXTRACT(DAY FROM (NOW() - end_date_time)) <= 7
    ) AS Z ON Z.id_tayangan = F.id_tayangan  
    GROUP BY F.id_tayangan

    UNION

    SELECT S.id_tayangan, COALESCE(COUNT(start_date_time),0) AS total_view, \'series\' AS jenis
    FROM SERIES S
    LEFT OUTER JOIN (
      SELECT RN.id_tayangan, start_date_time, end_date_time
      FROM RIWAYAT_NONTON RN
      JOIN (
        SELECT id_tayangan, SUM(E.durasi) as total_durasi_series
        FROM SERIES S
        JOIN EPISODE E ON E.id_series = S.id_tayangan
        GROUP BY id_tayangan
      ) AS S2 ON S2.id_tayangan = RN.id_tayangan
      WHERE 
        EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * S2.total_durasi_series * 60
        AND EXTRACT(DAY FROM (NOW() - end_date_time)) <= 7
    ) RN ON S.id_tayangan = RN.id_tayangan
    GROUP BY S.id_tayangan
  ) AS V
  JOIN TAYANGAN T ON V.id_tayangan =  T.id
  ORDER BY V.total_view DESC
  LIMIT 10;
"""

GET_TAYANGAN_TERBAIK_LOCAL_LOGIN = """
  SELECT *
  FROM (
    SELECT F.id_tayangan, COALESCE(COUNT(start_date_time),0) AS total_view, \'film\' AS jenis
    FROM FILM F 
    LEFT OUTER JOIN (
      SELECT RN.id_tayangan, start_date_time, end_date_time
      FROM RIWAYAT_NONTON RN
      JOIN FILM F2 ON F2.id_tayangan = RN.id_tayangan
      WHERE 
        EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * F2.durasi_film * 60
        AND EXTRACT(DAY FROM (NOW() - end_date_time)) <= 7
    ) AS Z ON Z.id_tayangan = F.id_tayangan 
    GROUP BY F.id_tayangan

    UNION

    SELECT S.id_tayangan, COALESCE(COUNT(start_date_time),0) AS total_view, \'series\' AS jenis
    FROM SERIES S
    LEFT OUTER JOIN (
      SELECT RN.id_tayangan, start_date_time, end_date_time
      FROM RIWAYAT_NONTON RN
      JOIN (
        SELECT id_tayangan, SUM(E.durasi) as total_durasi_series
        FROM SERIES S
        JOIN EPISODE E ON E.id_series = S.id_tayangan
        GROUP BY id_tayangan
      ) AS S2 ON S2.id_tayangan = RN.id_tayangan
      WHERE 
        EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * S2.total_durasi_series * 60
        AND EXTRACT(DAY FROM (NOW() - end_date_time)) <= 7
    ) RN ON S.id_tayangan = RN.id_tayangan
    GROUP BY S.id_tayangan
  ) AS V
  JOIN TAYANGAN T ON V.id_tayangan = T.id
  JOIN PENGGUNA P ON LOWER(P.negara_asal) = LOWER(T.asal_negara)
  WHERE P.username = %s
  ORDER BY V.total_view DESC
  LIMIT 10;
"""

GET_TAYANGAN_TERBAIK_LOCAL_GUEST = """
  SELECT *
  FROM (
    SELECT F.id_tayangan, COALESCE(COUNT(start_date_time),0) AS total_view, \'film\' AS jenis
    FROM FILM F 
    LEFT OUTER JOIN (
      SELECT RN.id_tayangan, start_date_time, end_date_time
      FROM RIWAYAT_NONTON RN
      JOIN FILM F2 ON F2.id_tayangan = RN.id_tayangan
      WHERE 
        EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * F2.durasi_film * 60
        AND EXTRACT(DAY FROM (NOW() - end_date_time)) <= 7
    ) AS Z ON Z.id_tayangan = F.id_tayangan 
    GROUP BY F.id_tayangan

    UNION

    SELECT S.id_tayangan, COALESCE(COUNT(start_date_time),0) AS total_view, \'series\' AS jenis
    FROM SERIES S
    LEFT OUTER JOIN (
      SELECT RN.id_tayangan, start_date_time, end_date_time
      FROM RIWAYAT_NONTON RN
      JOIN (
        SELECT id_tayangan, SUM(E.durasi) as total_durasi_series
        FROM SERIES S
        JOIN EPISODE E ON E.id_series = S.id_tayangan
        GROUP BY id_tayangan
      ) AS S2 ON S2.id_tayangan = RN.id_tayangan
      WHERE 
        EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * S2.total_durasi_series * 60
        AND EXTRACT(DAY FROM (NOW() - end_date_time)) <= 7
    ) RN ON S.id_tayangan = RN.id_tayangan
    GROUP BY S.id_tayangan
  ) AS V
  JOIN TAYANGAN T ON V.id_tayangan = T.id
  WHERE T.asal_negara ILIKE %s
  ORDER BY V.total_view DESC
  LIMIT 10;
"""

GET_ALL_FILM = "SELECT * FROM TAYANGAN WHERE id IN (SELECT id_tayangan FROM FILM);"

GET_ALL_SERIES = "SELECT * FROM TAYANGAN WHERE id IN (SELECT id_tayangan FROM SERIES);"

GET_FILM_BY_ID = """
  SELECT id, judul, sinopsis, asal_negara, id_sutradara, url_video_film, release_date_film, durasi_film, total_view, rating_rata_rata
  FROM (
      SELECT *
      FROM TAYANGAN
      WHERE id=%s
  ) AS T
  JOIN FILM  F ON F.id_tayangan=T.id
  JOIN (
    SELECT F2.id_tayangan, COUNT(start_date_time) AS total_view
    FROM RIWAYAT_NONTON RN
    RIGHT OUTER JOIN FILM F2 ON 
      RN.id_tayangan = F2.id_tayangan AND
      EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * F2.durasi_film * 60
    GROUP BY F2.id_tayangan
  ) FILM_VIEWS ON FILM_VIEWS.id_tayangan=T.id
  JOIN (
    SELECT id_tayangan, ROUND(AVG(rating),1) as rating_rata_rata
    FROM ULASAN U
    GROUP BY id_tayangan
  ) AVERAGE_RATING ON AVERAGE_RATING.id_tayangan=T.id;
"""

GET_SERIES_BY_ID = """
  SELECT id, judul, sinopsis, asal_negara, id_sutradara, total_view, rating_rata_rata
  FROM (
      SELECT *
      FROM TAYANGAN
      WHERE id=%s
  ) AS T
  JOIN SERIES S ON S.id_tayangan=T.id
  JOIN (
    SELECT S.id_tayangan, COUNT(start_date_time) AS total_view
    FROM RIWAYAT_NONTON RN
    RIGHT OUTER JOIN (
      SELECT id_tayangan, SUM(E.durasi) as total_durasi_series
      FROM SERIES S
      JOIN EPISODE E ON E.id_series = S.id_tayangan
      GROUP BY id_tayangan
    ) S ON 
      RN.id_tayangan = S.id_tayangan AND
      EXTRACT(EPOCH FROM end_date_time - start_date_time) >= 0.7 * S.total_durasi_series * 60
    GROUP BY S.id_tayangan
  ) SERIES_VIEWS ON SERIES_VIEWS.id_tayangan=T.id
  JOIN (
    SELECT id_tayangan, ROUND(AVG(rating),1) as rating_rata_rata
    FROM ULASAN U
    GROUP BY id_tayangan
  ) AVERAGE_RATING ON AVERAGE_RATING.id_tayangan=T.id;
"""

GET_SUTRADARA = '''
    SELECT *
    FROM CONTRIBUTORS
    WHERE id=%s;
'''

GET_GENRE = 'SELECT GT.genre FROM GENRE_TAYANGAN GT WHERE GT.id_tayangan=%s;'


GET_PEMAIN = '''
    SELECT *
    FROM MEMAINKAN_TAYANGAN MT
    JOIN CONTRIBUTORS C ON MT.id_pemain=C.id
    WHERE MT.id_tayangan=%s;
'''

GET_PENULIS_SKENARIO = '''
    SELECT *
    FROM MENULIS_SKENARIO_TAYANGAN MST
    JOIN CONTRIBUTORS C ON MST.id_penulis_skenario=C.id
    WHERE MST.id_tayangan=%s;
'''

GET_EPISODES_OF_SERIES = '''
    SELECT *
    FROM EPISODE
    WHERE id_series=%s;
'''

GET_ULASAN = '''
  SELECT * FROM ULASAN WHERE id_tayangan = %s ORDER BY timestamp DESC;
'''

GET_EPISODE_BY_SUBJUDUL = '''
  SELECT id_series, judul, E.*
    FROM (
      SELECT * 
      FROM EPISODE
      WHERE id_series=%s AND sub_judul=%s
    ) AS E
    JOIN TAYANGAN T ON T.id=E.id_series;
'''


GET_OTHER_EPISODES = '''
  SELECT * 
  FROM EPISODE
  WHERE id_series=%s AND sub_judul<>%s;
'''


SEARCH_TAYANGAN = '''
  SELECT T.*, \'series\' AS jenis
  FROM tayangan T
  JOIN series ON T.id = series.id_tayangan
  WHERE judul ILIKE %(searchkey)s

  UNION

  SELECT T.*, \'film\' AS jenis
  FROM tayangan T
  JOIN film ON T.id = film.id_tayangan
  WHERE judul ILIKE %(searchkey)s;  
'''

GET_DURASI_TAYANGAN = '''
  SELECT id_tayangan as id, durasi_film as durasi
  FROM film
  WHERE id_tayangan=%(id)s

  UNION

  SELECT id_series as id, SUM(durasi) as durasi
  FROM episode
  WHERE id_series=%(id)s
  GROUP BY id_series;
'''

ADD_RIWAYAT_NONTON = '''
  INSERT INTO riwayat_nonton (id_tayangan, username, start_date_time, end_date_time) VALUES (%s, %s, %s, %s);
'''