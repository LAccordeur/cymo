import happybase
import time

connection = happybase.Connection('127.0.0.1')


def create_table(connection, table_name, column_name):
    connection.create_table(
        table_name,
        {
            column_name:dict(),
        }
    )

    print("finish create table: " + table_name)

def create_table_with_2cf(connection, table_name, column1_name, column2_name):
    connection.create_table(
        table_name,
        {
            column1_name:dict(),
            column2_name:dict(),
        }
    )

    print("finish create table: " + table_name)


def put_batch(datas, connection, table=None):

        t = connection.table(table)

        b = t.batch(transaction=False)
        for row, data in datas.items():
            b.put(row, data)
        b.send()

def test():
    datas = dict()
    for i in range(100):
        article_type_id = i % 2
        timestamp = time.time() + i
        rowkey = "ARTICLE" + str(timestamp * 1000000)
        data = {
            "basic:" + "ArticleID": str(i),
            "basic:" + "ArticleTypeID": str(article_type_id),
            "basic:" + "Created": str(timestamp),
        }
        datas[rowkey] = data
    for row, data in datas.items():
        print(row)
        print(data)



if __name__ == "__main__":
    # create_table(connection, "python_test", "cf")
    # table = connection.table("python_test")

    datas = dict()
    datas["test"] = {"cf:test": str(2)}
    put_batch(datas, connection, "python_test")
    print()