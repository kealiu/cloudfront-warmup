# Usage

Cloudfront is the CDN of AWS. In the following case, you may want speed up the user experience in the first time when content updated:

1. new content added: this script touch each of the CDN edge pop and make the contents cached in them.
1. contents updated: you need to [invalidate these contents](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html) firstly, and then use this script.

## usage

1. a text file, named as CNAME of your cloudfront distribution, with file path per line in it
1. `python warmup.py <dxxxxxxxxxx.cloudfront.net> <cname.mydomain.com> [GET|HEAD|OPTION]`
    - the `HEAD`/`OPTION` only used in special case, default is `GET`
    - if no CNAME defined, just use the `dxxxxxxxxxx.cloudfront.net` as CNAME
1. if you distribution has many CNAME, and many actions, you can write your owner shell loop to execute it, this script ONLY for one CNAME & action in one time

## setup environment

1. [download & install python3.8](https://wiki.python.org/moin/BeginnersGuide/Download)
1. install dependences:
    ```
    pip install -r requestments.txt
    ```
1. edit `cname.mydomain.com` , one url path per line. 
1. (optional) update cloudfront edge pop information
   ```
   # global cloudfront
   python edgecode.py
   # in case china mainland cloudfront
   python edgecode.py mainland
   ```
1. (optional) if you know new edge code, just add it into `edges.global.json` or `edges.mainland.json` accordingly.
1. run this script with your distribution's `cloudfront.net` (`cloudfront.cn` in China) domain
    ```
    python warmup.py dxxxxxxxxxx.cloudfront.net cname.mydomain.com GET 2>/dev/null
    ```

**THE URL FILE MUST NAMED AS CLOUDFRONT CNAME**

# configuration

in the `warmup.py`, you can see the configurations:
```
{
    "http": True,   # enable http url
    "https": True,  # enable https url
    "mainland": False,  # in case china mainland cloudfront
    "threads": 200,  # how many threads 
    "timeout": (3,3),  # url connection timeout
    "origin": "",   # origin domain(optional)
    "cname" : "",    # the cname
    "action": "GET", # the http action
    "pops" : {
        "global": "edges.global.json",    # the pop config file of global cloudfront
        "mainland": "edges.mainland.json"  # the pop config file of china mainland cloudfront
    }
}
```

# Reference
[nwcd-samples cloudfront warmup](https://github.com/nwcd-samples/cloudfront-prewarm/)
