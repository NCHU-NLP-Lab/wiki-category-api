# -*- coding: utf-8 -*-
from opencc import OpenCC

if __name__ == '__main__':

    ans = input(
        "Are you sure? extract.txt will be overwrite if you do that! Enter y to insure: ")
    if ans != "y" and ans != "Y":
        exit()

    data_path = r"data\zhwiki-20211020-categorylinks.sql\zhwiki-20211020-categorylinks.sql"
    output_path = r"extract.txt"
    count = 0
    ex_line = 0
    mode = False
    stop_words = ["存檔", "模板", "條目", "頁面", "語句", "鏈接", "引文格式", "CS1", "重定向",
                  "的分類", "主題首頁", "規範控制", "有爭議的作品", "信息框", "導航框", "版權有問題", "維基人", "消歧義"]

    cc = OpenCC('s2tw')

    with open(output_path, "w", encoding="utf-8") as fo:
        with open(data_path, 'rb') as f:
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
                            # print(category_coverted, entity_converted)
                            fo.write(
                                f"{category_coverted}<->{entity_converted}\n")
                            ex_line += 1

                if count == -1:
                    break

    print("extract complete!")
    print(f"extract line: {ex_line}")
