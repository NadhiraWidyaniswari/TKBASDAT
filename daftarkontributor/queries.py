contributors_all_query = """
  SELECT 
    CONTRIBUTORS.id, 
    CONTRIBUTORS.nama, 
    CONTRIBUTORS.kewarganegaraan, 
    CASE WHEN CONTRIBUTORS.jenis_kelamin = 0 THEN 'Laki-laki' ELSE 'Perempuan' END AS jenis_kelamin,
    CONCAT_WS(', ', 
      CASE WHEN CONTRIBUTORS.id IN (SELECT P.id FROM PEMAIN P) THEN 'pemain' ELSE NULL END,
      CASE WHEN CONTRIBUTORS.id IN (SELECT S.id FROM SUTRADARA S) THEN 'sutradara' ELSE NULL END,
      CASE WHEN CONTRIBUTORS.id IN (SELECT PS.id FROM PENULIS_SKENARIO PS) THEN 'penulis_skenario' ELSE NULL END
    ) AS tipe
  FROM CONTRIBUTORS
"""


contributors_by_type_query = """
  SELECT 
    CONTRIBUTORS.id, 
    CONTRIBUTORS.nama, 
    CONTRIBUTORS.kewarganegaraan, 
    CASE WHEN CONTRIBUTORS.jenis_kelamin = 0 THEN 'Laki-laki' ELSE 'Perempuan' END AS jenis_kelamin,
    CONCAT_WS(', ', 
      CASE WHEN CONTRIBUTORS.id IN (SELECT P.id FROM PEMAIN P) THEN 'pemain' ELSE NULL END,
      CASE WHEN CONTRIBUTORS.id IN (SELECT S.id FROM SUTRADARA S) THEN 'sutradara' ELSE NULL END,
      CASE WHEN CONTRIBUTORS.id IN (SELECT PS.id FROM PENULIS_SKENARIO PS) THEN 'penulis_skenario' ELSE NULL END
    ) AS tipe
  FROM CONTRIBUTORS
  JOIN {table} ON CONTRIBUTORS.id = {table}.id;
"""