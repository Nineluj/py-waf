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
   
4. Validate the config. A sample config is provided in `config/config.sample.yml`

5. Run `./run.py --config <path to config>`

## Testing app

### For Docker
1. Run the testing container
    ```
    docker run -it --name vuln_app -p 4040:4040 santosomar/vuln_app:latest /bin/bash
    ```

2. Run the WAF
    ```shell script
   docker run -v <local>:<container> -it pywaf --config <path_to_config> 
    ```

### With Podman
1. Run the testing container
    ```shell script
    podman run -it --name vuln_app --pod new:waf -p 4040:4040 -p 9991:80 santosomar/vuln_app:latest /bin/bash
    ```
2. Run the WAF
    ```shell script
   podman run -it --pod waf -v <local>:/tmp/dir --rm pywaf -c /tmp/dir/config.yml
    ```