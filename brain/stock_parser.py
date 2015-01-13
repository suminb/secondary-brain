# -*- coding: utf-8 -*-
"""Provides an interface for stock parsers."""

class StockParser(object):
    # FIXME: These properties probably should be under a difference class.
    # For example, StockQuote or something like that.
    @property
    def symbol(self):
        """Stock symbol (e.g., AMZN, YHOO, 035720.KQ)"""
        raise NotImplementedError()

    @property
    def trading_periods(self):
        """A list of trading periods (may be more than one)"""
        raise NotImplementedError()

    @property
    def granularity(self):
        """Data granularity (e.g., 1 sec, 1 min, 1 day, etc.)"""
        raise NotImplementedError()

    @property
    def quotes(self):
        """A list of (datetime, volume, open, close, low, high) tuples"""
        raise NotImplementedError()