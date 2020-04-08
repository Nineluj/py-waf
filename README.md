# py-waf - A python WAF

## Setup for local development
1. Create venv for Python 3.8 (in the root directory of the project)
    ```shell script
   python --version
   > ... 3.8 ...
   python -m venv venv
    ```
2. Active the venv in your shell
    ```shell script
   source venv/bin/activate
    ```
3. Install the requirements
    ```shell script
   pip install -r requirements.txt 
   ```
 ## Testing app
 1. Run this container like so
    ```
    docker run --rm -it -p 8080:80 vulnerables/web-dvwa
    ```