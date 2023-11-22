#!/usr/bin/expect -f

while true; do
    # Run the scp command here
    sshpass -p 'oNVKMXlvmj1' scp -r ubuntu@188.213.199.150:/home/ubuntu/crawl_and_match/best-images/* ./images/candidates
    sshpass -p 'oNVKMXlvmj1' scp -r ubuntu@188.213.199.150:/home/ubuntu/crawl_and_match/best-images/* ./images/candidates
    sshpass -p 'oNVKMXlvmj1' scp -r ubuntu@188.213.199.150:/home/ubuntu/crawl_and_match/best-images/* ./images/candidates
    # Sleep for 30 seconds
    sleep 5
done