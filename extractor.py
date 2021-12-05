# -*- coding: utf-8 -*-
from opencc import OpenCC

if __name__ == '__main__':

    file_path = r"data\zhwiki-20211020-categorylinks.sql\zhwiki-20211020-categorylinks.sql"
    count = 0
    mode = False
    stop_words = ["存檔", "模板", "條目", "頁面", "語句", "鏈接", "引文格式", "CS1"]

    cc = OpenCC('s2tw')

    with open(file_path, 'rb') as f:
        for line in f:
            # print(line[:100])
            if line[:11] == b'INSERT INTO':
                mode = True
            else:
                mode = False

            if mode:
                count += 1
                print("count:", count)
                sql = line.decode('utf-8', errors='ignore')
                # print(sql)
                rows = sql.split("),(")
                for i, row in enumerate(rows):
                    # print("row:", row)
                    if i == 0:
                        row = row.split("VALUES (")[1]

                    cols = row.split("','")
                    category = cols[0].split(",'")[1]
                    entity = cols[1]
                    if '\\n' in entity:
                        entity = entity.split('\\n')[1]

                    category_coverted = cc.convert(category)
                    entity_converted = cc.convert(entity)

                    is_stop = False
                    for stop_word in stop_words:
                        if stop_word in category_coverted:
                            is_stop = True
                            break
                    
                    if not is_stop:
                        print(category_coverted, entity_converted)


            if count == 1:
                break

    print("count:", count)
