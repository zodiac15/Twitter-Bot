s = open('latest.txt', 'r+')
since_id = int(s.readline())
while True:
    since_id = since_id + 1
    print(since_id)
    s.seek(0)
    s.write(str(since_id))
    s.close()