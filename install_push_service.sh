#!/bin/sh
mkdir /opt/temp_dynamodb
chmod 775 -R /opt/temp_dynamodb
chown -R nobody /opt/temp_dynamodb

cp rtl_433_Local_File.py /opt/temp_dynamodb
cp push_data_DynamoDB.py /opt/temp_dynamodb

cp push_data_DynamoDB.service /etc/systemd/system
cp rtl_433_Local_File.service /etc/systemd/system

systemctl enable push_data_DynamoDB
systemctl enable rtl_433_Local_File

systemctl start push_data_DynamoDB
systemctl start rtl_433_Local_File
s