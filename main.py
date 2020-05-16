import mysql.connector
import json

database = ""
rawtable = ""
wptable=""
post_author_id=""


def fetchjsondata(uuid):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database=database
    )
    dbcursor = conn.cursor()
    dbcursor.execute("SELECT data FROM " + rawtable + " WHERE uuid=" + uuid)
    resultset = dbcursor.fetchone()

    jsondata = resultset[0]
    return jsondata

def extractjsonvalues(jsonobject):
    jsondata=json.loads(jsonobject)
    title=jsondata["question"]["title"]
    body=jsondata["question"]["body"]
    url=jsondata["question"]["path"]["path"]
    values={
        "post_title":title,
        "post_content":body,
        "title_slug":url
    }
    return values

def publish():
    post_content=""
    post_title=""
    post_name=""
    sqlstatement="INSERT INTO `"+wptable+"` (`ID`, `post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) VALUES (NULL, '"+post_author_id+"', now(), now(), '"+post_content+"', '"+post_title+"', '', 'publish', 'open', 'open', '', '"+post_name+"', '', '', now(), now(), '', '0', '', '0', 'post', '', '0')"

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database=database
    )
    dbcursor = conn.cursor()
    dbcursor.execute(sqlstatement)
    conn.commit()
    print(dbcursor.rowcount, "record inserted.")

def mark_done(uuid):
    #todo
    pass

def helpers():
    #todo check if raw database has a 'done' column and add
    #todo check if all questions are marked as done and exit if yes
    #todo check if author_id matches te provided id and update where necessary
    pass