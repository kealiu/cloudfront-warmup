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
1. run this script with your distribution's `cloudfront.net` (`cloudfront.cn` in China) domain
    ```
    python warmup.py dxxxxxxxxxx.cloudfront.net cname.mydomain.com GET 2>/dev/null
    ```

**THE URL FILE MUST NAMED AS CLOUDFRONT CNAME**

# configuration

in the `warmup.py`, you can see the configurations:
```
{
    "pops": {
        "addones": [],  # in case you find new edge-pop code
        "source": "https://www.feitsui.com/zh-hans/article/3",  # the sources of edge-pop code
        "china": ['BJS9-E1', 'PVG52-E1', 'SZX51-E1', 'ZHY50-E1']  # the sources of edge-pop code for china
     },
    "http": True,   # enable http url
    "https": False,  # enable https url
    "china": False,  # in case china cloudfront
    "threads": 200,  # how many threads 
    "timeout": 10,  # url connection timeout
}
```

# Reference
[nwcd-samples cloudfront warmup](https://github.com/nwcd-samples/cloudfront-prewarm/)
