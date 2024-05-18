CREATE_ULASAN = '''
  INSERT INTO ULASAN (id_tayangan, username, timestamp, rating, deskripsi)
  VALUES (%s, %s, NOW(), %s, %s);
'''
