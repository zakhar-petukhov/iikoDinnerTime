# How to use all scripts?

If this is a new server, you must first create the keys:
1) key for GitHub, run "create_ssh_keys.sh".
2) private key and public key for encoding and decoding the dump, run "create_openssl_keys.sh".

Then run the script "setup.sh" to install docker and other dependencies

The scripts "start.sh" and "stop.sh" are designed to start and stop the server (by default production). To start the developer environment you need to add the tag dev ---> exp: ./start.sh dev.  

The script "update.sh" is designed to update the code (copies the code from GitHub and creates a new image in DockerHub),
 "update.sh" can accept the second parameter (tag): one decimal place ---> production (1.0), two decimal places (1.00).
