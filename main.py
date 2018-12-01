#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os

import json

import crawler

class main:
	def __init__(self, domain, output):
		self.domain = domain
		self.output = output

	def main(self):
		dict_arg = {}
		dict_arg['skipext'] = []
		dict_arg['num_workers'] = 1
		dict_arg['parserobots'] = False
		dict_arg['debug'] = False
		dict_arg['verbose'] = False
		dict_arg['exclude'] = []
		dict_arg['drop'] = []
		dict_arg['report'] = False
		dict_arg['images'] = False
		dict_arg['domain'] = self.domain
		dict_arg['output'] = self.output
		crawl = crawler.Crawler(**dict_arg)
		crawl.run()

		pass
