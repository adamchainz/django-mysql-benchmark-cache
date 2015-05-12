Django-MySQL benchmark cache
============================

For benchmarking the cache backend from django-mysql against memcached.

Usage
-----

1. `pip install -r requirements.txt`
2. Have MySQL/MariaDB and memcached running locally.
3. `mysql -e 'create database benchmark_cache'`
4. `python manage.py migrate`
4. `python manage.py createcachetable`
4. `python manage.py benchmark_caches`

Benchmark
---------

Really simple, it just hammers out a few operations with randomly sized data.

Output
------

Something like this:

```
+----------------+--------------------+
| Cache          | Time for benchmark |
+----------------+--------------------+
| DatabaseCache  |             54.635 |
+----------------+--------------------+
| PyLibMCCache   |              2.988 |
+----------------+--------------------+
| MySQLCache     |              8.396 |
+----------------+--------------------+
| MemcachedCache |              3.207 |
+----------------+--------------------+
```
