#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/6/17 15:31
# @Author:  haiyong
# @File:    test_click.py
import string

import click

@click.command()
@click.option('--field', '-f', help='字段')
# @click.option('--display-filter', '-Y', prompt='display-filter', nargs=2, help='条件')
@click.option('--display-filter', '-Y', prompt='display-filter', type=(str, int, float, bool), help='条件')
@click.option('--count', '-c', default=2, prompt='count', help='条件')
def cli(field, display_filter,count):
    """Simple program that greets NAME for a total of COUNT times."""

    click.echo(f'{field} {display_filter} {count}')

if __name__ == '__main__':
    cli()








