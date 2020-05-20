import mysql.connector
import json

database = "spyder"
rawtable = "questions"
wptable = "wp_questions"
post_author_id = "1"
rowcount = 1025270
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database=database
)


def isdone(id):
    dbcursor = conn.cursor()
    dbcursor.execute("SELECT published_at FROM", rawtable, "WHERE id=", id,"AND published_at=NULL")
    if dbcursor.rowcount == 0:
        return True
    else:
        return False


def fetch_jsondata(id):
    dbcursor = conn.cursor()
    dbcursor.execute("SELECT data FROM", rawtable, "WHERE id=", id)
    resultset = dbcursor.fetchone()

    jsondata = resultset[0]
    return jsondata


def extractjsonvalues(jsonobject):
    jsondata = json.loads(jsonobject)
    title = jsondata["question"]["title"]
    body = jsondata["question"]["body"]
    url = jsondata["question"]["path"]["path"]
    values = {
        "post_title": title,
        "post_content": body,
        "title_slug": url
    }
    return values


def publish(values: dict):
    post_content = values["post_title"]
    post_title = values["post_content"]
    post_name = values["title_slug"]
    sqlstatement = "INSERT INTO ", wptable, " ('ID', 'post_author', 'post_date', 'post_date_gmt', 'post_content', 'post_title', 'post_excerpt', 'post_status', 'comment_status', 'ping_status', 'post_password', 'post_name', 'to_ping', 'pinged', 'post_modified', 'post_modified_gmt', 'post_content_filtered', 'post_parent', 'guid', 'menu_order', 'post_type', 'post_mime_type', 'comment_count') VALUES (NULL, '", post_author_id, "', now(), now(), '", post_content, "', '", post_title, "', '', 'publish', 'open', 'open', '', '", post_name, "', '', '', now(), now(), '', '0', '', '0', 'post', '', '0')"

    dbcursor = conn.cursor()
    dbcursor.execute(sqlstatement)
    conn.commit()
    print(dbcursor.rowcount, "record(s) inserted.")


def mark_done(id):
    print("Marking id ", id, "as done!")
    dbcursor = conn.cursor()
    dbcursor.execute("UPDATE", rawtable, "SET published_at=now() WHERE id=", id)
    conn.commit()
    print(dbcursor.rowcount, "record(s) affected")


def check_author():
    print("Checking and Updating author...")
    dbcursor = conn.cursor()
    # todo check if author_id matches the provided id and update where necessary
    dbcursor.execute("UPDATE", wptable, "SET post_author=", post_author_id, " WHERE post_author!=", post_author_id)
    conn.commit()
    print(dbcursor.rowcount, "record(s) affected")


def addcolumn():
    # todo check if raw database has a 'done' column and add
    dbcursor = conn.cursor()
    dbcursor.execute("ALTER TABLE", rawtable, "ADD done BOOLEAN NOT NULL DEFAULT 'false' WITH VALUES")
    print("Added 'done' column")
    print(dbcursor.rowcount, "record(s) affected")


# Starts here
if __name__ == "__main__":
    # todo check connection on every loop
    addcolumn()
    # fetch raw data for every row
    for i in range(rowcount):
        # if rowexists(i):
        if not isdone(i):
            data = fetch_jsondata(i)
            values = extractjsonvalues(data)
            publish(values)
            mark_done(i)
        # else:
        # print("raw ",i,"does not exist")
        # continue
    pass
