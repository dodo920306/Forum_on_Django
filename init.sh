#!/bin/bash


sudo systemctl start docker
sudo systemctl enable docker
sudo docker volume create django_forum_postgres_data
sudo docker volume create django_forum_static_volume
sudo docker volume create django_forum_media_volume
echo "請輸入電子郵件："
read email
echo "請輸入應用程式密碼："
read -s password
echo "請輸入網站連接埠："
read port

# 取代 .env 檔案中的 EMAIL_USER 和 EMAIL_PASSWORD 欄位
sed -i "s/EMAIL_USER=.*/EMAIL_USER=$email/" .env
sed -i "s/EMAIL_PASSWORD=.*/EMAIL_PASSWORD=$password/" .env
sed -i "s/^PORT=.*/PORT=$port/" .env
sed -i "s/\${port}/$port/" docker-compose.yml
