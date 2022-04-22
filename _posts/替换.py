import re 

f = open("./2022-04-22-Rosnotes-post.md", 'r', encoding="utf-8")
f1 = open("2022-04-24-Rosnotes-post.md", "w", encoding="utf-8")

md = f.readlines()
# print(md)
for i in range(len(md)):
    r = re.findall("./img/%E5%9B%BE%E7%89%87", md[i])
    if len(r)>0:
        md[i] = md[i].replace('./img/%E5%9B%BE%E7%89%87', '../style/img/img/%E5%9B%BE%E7%89%87')
        # print(md[i])
    f1.write(md[i])

print('over!')

f.close()
f1.close()