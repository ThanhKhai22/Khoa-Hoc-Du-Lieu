import requests
from bs4 import BeautifulSoup
 
url = "https://edition.cnn.com/2021/10/03/uk/everard-uk-police-gbr-cmd-intl/index.html"
 
# Gửi 1 request đến url phía trên và nhận lại source page của nó
r = requests.get(url)
 
print(r.status_code) # 200 là thành công
 
# In thử page source ra coi sao, mình in thử 1000 ký tự đầu tiên thôi
# Bạn có thể thử so sánh với source mà bạn thấy trên trình duyệt
print(r.content[:1000])
 
 
# Làm đẹp source 
# Mình dùng lxml parser cho nhanh, 
# Ngoài ra có html.parser, lxml-xml, html5lib (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
soup = BeautifulSoup(r.content, 'lxml')
 
print("============TITLE=============")
# Lấy thẻ tiêu đề bài báo
print(soup.title)
# Lấy nội dung tiêu đề
print(soup.title.text)
 
# Lấy ảnh đại diện của bài báo
# Ta tìm selector của nó theo hướng dẫn ở trên rồi dùng hàm select_one để tìm 1 phần tử đầu tiên
print("============FEATURE IMAGE=============")
feature_image = soup.select_one('#large-media > div > img')
print(feature_image.get('data-src-large'))
 
 
# Lấy nội dung bài
print("============CONTENT=============")
# Mình kiểm tra phần tử thì thấy nội dung bài nằm trong section id="body-text"
content_ele = soup.select_one("#body-text")
print(content_ele.text)
 
# Lấy tác giả bài viết, ngay phía dưới tiêu đề và phía trên ảnh đại diện
# By Kara Fox, CNN
print("============AUTHOR=============")
author_ele = soup.select_one('body > div.pg-right-rail-tall.pg-wrapper > article > div.l-container > div.metadata > div > p.metadata__byline > span > a')
print(author_ele.text)