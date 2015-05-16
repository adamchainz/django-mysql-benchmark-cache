# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from collections import OrderedDict
import time
from random import randint

from django.conf import settings
from django.core.cache import caches
from django.core.management import BaseCommand
from django.utils import six
from texttable import Texttable


class Command(BaseCommand):
    args = "<cache_alias>"

    help = """Benchmarks the caches."""

    def handle(self, *aliases, **kwargs):
        results = {}
        for alias in settings.CACHES:

            # The alias 'default' isn't very explanatory, so ignore it
            if alias == 'default':
                continue

            # Aliases specified on commandline = filter
            if aliases and alias not in aliases:
                continue

            results.update(self.do_benchmark(alias))

        self.output_results(results)

    def do_benchmark(self, alias):
        cache = caches[alias]
        self.stdout.write("Benchmarking {}".format(alias))

        cache.clear()
        timings = OrderedDict()

        # sets
        start = time.time()
        for i in six.moves.range(1000):
            cache.set(self.random_key(), self.random_binary())
        timings['set'] = time.time() - start

        # set_manys
        start = time.time()
        for i in six.moves.range(1000):
            cache.set_many({
                self.random_key(): self.random_binary()
                for x in six.moves.range(40)
            })
        timings['set_many'] = time.time() - start

        # gets
        start = time.time()
        for i in six.moves.range(1000):
            cache.get(self.random_key())
        timings['get'] = time.time() - start

        # get_many
        start = time.time()
        for i in six.moves.range(1000):
            cache.get_many([
                self.random_key()
                for x in six.moves.range(40)
            ])
        timings['get_many'] = time.time() - start

        return {alias: timings}

    def random_key(self):
        return "Key{}".format(randint(1, 500))

    def random_binary(self):
        return randint(1, 1024 ** 1) * six.binary_type(randint(0, 255))

    def output_results(self, results):
        table = Texttable(max_width=0)

        header = ["Cache Alias"]
        for key in next(six.itervalues(results)):
            header += ["{} benchmark".format(key)]
        table.add_row(header)
        table.set_cols_align(["l"] + (["r"] * (len(header) - 1)))

        for alias, timings in six.iteritems(results):
            row = [alias]
            for benchmark, total in six.iteritems(timings):
                row += ['{}'.format(total)]
            table.add_row(row)

        self.stdout.write(table.draw())
