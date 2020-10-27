# Temperature Reading

This is a simple project to read the temperature sensors in my house and push the information to a DynamoDB table in AWS

This project need a RTL-SDR compatible dongle, and uses the [rtl_433](https://github.com/merbanan/rtl_433/) project to read the values and send the reading as a Syslog message to the parser.

There is 2 Syslog parsers:
* **rtl_433_DynamoDB.py**: Receive the reading and push it to the DynamoDB table
* **rtl_433_Local_File.py**: Receive the reading and write ir to a file in a directory, need a secondary script to push the info to the DynamoDB - **push_data_DynamoDB.py**

The files are stored into the **tempread** sub directory

To read the sensors we jsut need to run the following command:
`rtl_433 -C si -F syslog:127.0.0.1:1433`
