# redis-treemap

Visualise the size of your Redis database in a fancypants interactive treemap.

## Prerequisites

This tool assumes you're using the colon-delimited key format that is common among Redis users; if you have keys of the form `foo:123` and `bar:456`, it will show the sizes of foo and bar and let you zoom in to inspect.

## How to use

1. Clone the repository somewhere. We suggest setting up a slave of your main instance, and running the tool on that. (If you're worried about the size of your data then you probably don't want to risk locking up your live server.)
2. You might need to run `pip install redis` if you don't have the [library](https://pypi.python.org/pypi/redis/) handy
3. Edit `generate.py` with your Redis server's details
4. Run `python generate.py` to create a data.json file
5. Open view/index.html in a browser (perhaps using Python's [SimpleHTTPServer](https://docs.python.org/2/library/simplehttpserver.html)
6. Revel in the treemap magic, and figure out who's filling up your database

## TODOs

* Only counts things that are strings, which is what we have, but we're not normal people
* Doesn't support Redis authentication, Redis Cluster, or various other fancy features
* Sends the `keys *` command, which is bad
* Is rather slow if you have [actual big data](https://twitter.com/wtrsld/status/424272437929205760)
* Later: this seems like a sensible use for a graph database
