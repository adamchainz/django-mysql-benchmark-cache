# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import time
from random import randint

from django.conf import settings
from django.core.cache import caches
from django.core.management import BaseCommand
from django.utils import six
from texttable import Texttable


class Command(BaseCommand):
    help = """Benchmarks the caches."""

    def handle(self, *args, **kwargs):
        results = {}
        for alias in settings.CACHES:

            # The alias 'default' isn't very explanatory, so ignore it
            if alias == 'default':
                continue

            results.update(self.do_benchmark(alias))

        self.output_results(results)

    def do_benchmark(self, alias):
        cache = caches[alias]
        name = cache.__class__.__name__
        self.stdout.write("Benchmarking {}".format(name))

        cache.clear()

        start = time.time()

        # sets
        for i in six.moves.range(1000):
            cache.set(self.random_key(), self.random_binary())

        # set_manys
        for i in six.moves.range(1000):
            cache.set_many({
                self.random_key(): self.random_binary()
                for x in six.moves.range(40)
            })

        # gets
        for i in six.moves.range(1000):
            cache.get(self.random_key())

        # get_many
        for i in six.moves.range(1000):
            cache.get_many([
                self.random_key()
                for x in six.moves.range(40)
            ])

        end = time.time()

        return {name: (end - start)}

    def random_key(self):
        return "Key{}".format(randint(1, 500))

    def random_binary(self):
        return randint(1, 1024 ** 1) * six.binary_type(randint(0, 255))

    def output_results(self, results):
        table = Texttable()
        table.set_cols_align(["l", "r"])
        table.add_row(["Cache", "Time for benchmark"])

        for name, benchmark_time in six.iteritems(results):
            table.add_row([name, '{}'.format(benchmark_time)])

        self.stdout.write(table.draw())
