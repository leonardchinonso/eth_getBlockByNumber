
# eth_getBlockByNumberWithCache

---
eth_getBlockByNumberWithCache is a caching proxy for CloudFlare's eth_getBlockByNumber method. It makes use of the LRU caching style as its cache
method. It is built using Python's flask framework and uses REST as its communication method.

eth_getBlockByNumberWithCache exposes four(4) [endpoints](https://documenter.getpostman.com/view/7575343/Tzm3nxRV) with which the API
can be accessed.

## Installation

There are three ways to install this app for use:
+ Dockerfile
+ Docker pull
+ Local machine

To use any of the Docker enabled methods above, you must have Docker installed.

For Mac users, install with this [link](https://docs.docker.com/docker-for-mac/install/)

For Windows users, install with this [link](https://docs.docker.com/docker-for-windows/install/)

To use the last method, you must have python and pip installed on your local machine.

### - Dockerfile
Firstly, clone this git repo and you should be at the project's root directory. If you're not, navigate to it using the command below.
```bash
cd /path/to/eth_getBlockByNumber
```
Build a Docker image with the following command:
```bash
docker build --tag eth_get_block_by_number .
```
Now, go ahead and run this image as a container using:
```bash
docker run --publish 5000:5000 eth_get_block_by_number
```
Using this command will however kill the process when you exit the shell or CLI running the container.
To keep the process running, use:
```bash
docker run -d -p 5000:5000 eth_get_block_by_number
```
The two ports specify the HOST and CONTAINER ports respectively. To run on a different port on your machine, change the
first port to your port number, i.e.
```bash
docker run -d -p PORT_NUMBER:5000 eth_get_block_by_number
```
To kill this process when done, run:
```bash
docker ps
```
Look for the container with IMAGE: *leonardchinonso/eth_get_block_by_number* and fetch the CONTAINER ID. Then run:
```bash
docker stop CONTAINER_ID
```

### - Docker pull
I already created a Docker image using the steps outlined above and pushed to a registry. All you need to do now is pull
this image and run containers from it.


Open your terminal and run:
```bash
docker pull leonardchinonso/eth_get_block_by_number:latest
```
This should have the image pulled into your local machine. 
Just like the steps from *Dockerfile* above, the next commands you run determine the lifespan of the process:
```bash
docker run --publish PORT_NUMBER:5000 eth_get_block_by_number
```
*OR*
```bash
docker run -d -p PORT_NUMBER:5000 eth_get_block_by_number
```

### - Local machine
If you're using Python 2.x, replace "python3" with "python" and "pip3" with "pip" in the commands below.

Clone this git repo and you should be at the project's root directory. If you're not, navigate to it using the command below.
```bash
cd /path/to/eth_getBlockByNumber
```
Add the .env file to the project's root directory.
Create a virtual environment with:
```bash
python3 -m venv .venv
```
Navigate to the Scripts folder with:
```bash
cd /.venv/Scripts
```
Activate the virtual environment with:
```bash
activate
```
Navigate to the project root folder with:
```bash
cd ../../
```
Install the packages with:
```bash
pip3 install -r requirements.txt
```
Finally, run the app with:
```bash
flask app
```

## Usage
After following the instructions for installation, your app should be up and running.

To access the endpoints...

+ Using cURL

In your terminal, run the command:
```bash
curl localhost:PORT_NAME
```

+ Using your browser

Navigate to *localhost:PORT_NAME* in your browser

To clear the cache, simply quit the application with *CTRL+C* and rerun it.

## Tests
The unit and integration tests can be individually run by navigating to the path of the specific test to be run and using the command:
```bash
python test_name.py
```
However, this can be a pain so a python file is included in the project's root directory called *test.py*. This runs all the
individual unit and integration tests at once to avoid the manual labour.

To execute the tests at once, navigate to the project root directory and run:
```bash
python test.py
```

## Assumptions
I had to make some assumptions while building the project. All these assumptions I outlined below:

1. I assumed that once a new block has been created, new transactions cannot be added to the previous block. This was important 
as getting transactions by index number was done with the array's index. So if a new transaction is added to a previous block
after the block has been cached, you won't be able to retrieve the latest transaction from it as it will raise an index
out of bounds exception.
2. I assumed that transaction indexes can not be more than 10 characters long. This was done because both the transaction's indexes
and hashes can be hexadecimal values. There has to be a way to differentiate them in order to get transactions by index or by hash value.


## Improvements
Apart from code quality and more automation, a lot of code improvements can be made to the existing application:

1. From *assumption-1* outlined above, when a call to get transaction by index is made to the API. If the index is invalid, we could
recheck the block by initiating a request to CloudFlare to see if any new transactions have been added. That way, we can totally
avoid making *assumption-1*.
2. From *assumption-2* outlined above, we could modify the endpoint to collect a query parameter of say "type", to know if the
user wants to query the transactions by index or by hash. That way, we eliminate the ambiguity of what is to be called.

## License
[MIT](https://choosealicense.com/licenses/mit/)
