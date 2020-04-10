# AWSome Gaming Server

This repository contains some scripts to help you run your own gaming server on AWS using Docker.
All servers are run using Docker to avoid having to make the configuration as easy a possible.

## IAM

I suggest creating a separate [IAM user](https://console.aws.amazon.com/iam/home#/users) that will perform actions on your EC2 instance and S3 bucket(s).
If also wish to allow someone else to access the resources on AWS, I recommend creating separate user accounts for them, too.

## S3 buckets

To store data in a reliable way, containers mount their data directories on [S3 buckets](https://s3.console.aws.amazon.com/s3/home).
This should be pretty inexpensive, but you're free to edit the scripts to save data directly on the instance.

## EC2

To run a small server for 4 people who want to play Minecraft and chat on TeamSpeak, you will need at least a `t3.small` instance.
Choose the region close to where you live and with the cheapest cost per hour.
Remember to shutdown the server when you are done playing, otherwise you might end up with a pricey bill at the end of the month.

### Security Groups

To keep your server safe, you will need to open only the ports you need.

The ports required by each server are listed in the [Servers](#servers) section.

### Policy

This is the policy required for the IAM user to read/write on a bucket

```json
{
  "Id": "<SERVER_NAME>_data_policy",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RetrieveBucket",
      "Action": [
        "s3:GetBucketLocation",
        "s3:ListBucket"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::<BUCKET_NAME>",
      "Principal": {
        "AWS": [
          "arn:aws:iam::<AWS_ACCOUNT_NUMBER>:user/<EC2_INSTANCE_USER>"
        ]
      }
    },
    {
      "Sid": "ReadWriteObjects",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::<BUCKET_NAME>/*",
      "Principal": {
        "AWS": [
          "arn:aws:iam::<AWS_ACCOUNT_NUMBER>:user/<EC2_INSTANCE_USER>"
        ]
      }
    }
  ]
}
```

You will need to add this policy in order for the EC2 instance to be able to perform any operation on the bucket. To add the policy:
1. Open https://s3.console.aws.amazon.com/s3/buckets/
2. Select your bucket
3. Click "Permissions", then "Bucket Policy"
4. Add the policy with the appropriate values
5. Click "Save"

## Servers

To run a specific server, you will just need to
1. Add port 22 (SSH) your server's Security Group
2. SSH into your EC2 instance, e.g. `ssh -i private_key.pem ec2-user@42.42.42.42`
2. Run `sudo ./configure.sh`
3. Run the server script, e.g. `./minecraft.sh`

Note: by running one of the servers listed here, you are accepting their respective licenses.
If you wish to read the licenses, please check the scripts.

### Minecraft
Default port: 25565

Source: https://github.com/itzg/docker-minecraft-server

### TeamSpeak
Default ports: 9987, 10011, 30033

Docker image: https://hub.docker.com/_/teamspeak 

## Contributing

Contributions are very welcome!

If you want to add another server or improve the existing scripts, please don't hesitate to submit a pull request!
