LOGIN = """
  SELECT P.username,P.password 
  FROM PENGGUNA as P
  WHERE P.username = %s AND P.password = %s;
"""

REGISTER = """
  INSERT INTO PENGGUNA(username,password,negara_asal)
  VALUES(%s,%s,%s);
"""
