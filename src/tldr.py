#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2023 Thomas Harr <xDevThomas@gmail.com>
# Copyright (c) 2017 www.chedanji.com

import datetime
import getopt
import json
import os
import re
import subprocess
import sys
import time

from workflow import Workflow, web

# GitHub repo for self-updating
UPDATE_SETTINGS = {'github_slug': 'harrtho/alfred-tldr'}

# GitHub Issues
HELP_URL = 'https://github.com/harrtho/alfred-tldr/issues'

# Cache Update frequency in days
CACHE_TTL = 7

default_platform = 'osx'


def query(query):
  global default_platform
  clone()

  dic = parse_args(query)
  isUpdate = dic['isUpdate']
  default_platform = dic['platform']
  command = dic['command']

  if bool(isUpdate):
    update()
    output_title('Update success')
  else:
    update(7)

  if(len(query) == 0):
    rowList = [{
      'uid': '1',
      'arg': '',
      'autocomplete': '',
      'icon': 'icon.png',
      'title': 'Please input',
      'valid': 'no'
    }]
  else:
    rowList = parse_man_page(command)
    if(len(rowList) == 0):
      rowList = hint(command, default_platform)
    if(len(rowList) == 0):
      rowList = [{
        'uid': '1',
        'arg': '',
        'autocomplete': '',
        'icon': 'icon.png',
        'title': 'Page not found',
        'valid': 'no'
      }]
  gen_feedback(rowList)


def find_page_location(command):
  index = wf.cached_data('index', download_index, CACHE_TTL * 86400)
  command_list = [item['name'] for item in index['commands']]
  if command not in command_list:
    return os.path.join(os.path.join(wf.cachedir, 'tldr', 'pages'),
                    os.path.join("common", command + '.md'))

  supported_platforms = index['commands'][
    command_list.index(command)]['platform']
  if default_platform in supported_platforms:
    platform = default_platform
  elif 'common' in supported_platforms:
    platform = 'common'
  else:
    platform = ''

  if not platform:
    return
  page_path = os.path.join(os.path.join(wf.cachedir, 'tldr', 'pages'),
                        os.path.join(platform, command + '.md'))
  return page_path

def parse_page(page):
  with open(page, encoding='utf-8') as f:
    lines = list(f)

  if (len(lines) <= 0):
    return []

  first_line = lines[0]
  if (first_line.startswith('#')):
    return parse_old_page(lines)
  else:
    return parse_new_page(lines)


def parse_old_page(lines):
  row_list = []
  uid = 1
  item = {}
  for line in lines:
    if line.startswith('#'):
      continue
    elif line.startswith('-'):
      item = {}
      item['uid'] = str(uid)
      item['subtitle'] = line.replace('-', '').replace(':', '').strip()
    elif line.startswith('`'):
      item['title'] = line.replace('`', '').replace('{{', '').replace('}}', '').strip()
      row_list.append(item)

    uid += 1
  return row_list


def parse_new_page(lines):
  row_list = []
  uid = 1
  item = {}
  code_pattern = re.compile(r'^( {4,} | \t)')
  subtext_pattern = re.compile(r'^\=?$')
  for line in lines:
    if (len(line.strip() == 0)):
      continue
    elif (code_pattern.match(line)):
      item[title] = line.replace('{{', '').replace('}}', '').strip()
      row_list.append(item)
    elif (subtext_pattern.match(line.rstrip())):
      continue
    else:
      item = {}
      item['uid'] = str(uid)
      item[subtitle] = line.strip()

    uid += 1

  return row_list


def parse_man_page(command):
  """Parse the man page if exist and return

  Args:
      command (str): The command whose man page is to be parsed

  Returns:
      list: Parsed sub-commands and description
  """
  page_path = find_page_location(command)
  if page_path and os.path.exists(page_path):
    return parse_page(page_path)
  return []


def gen_feedback(rowList):
  for row in rowList:
    wf.add_item(
      row.get('title') or '',
      row.get('subtitle') or '',
      row.get('title') or '',
      row.get('autocomplete') or '',
      False if row.get('valid') == 'no' else True,
      row.get('uid') or '',
      row.get('icon'))


def output_title(msg):
  wf.add_item(
    str(msg),
    uid=str(time.time()),
    icon='icon.png',
    valid=False)


def clone():
  """Clone the man page repository into the workflow cache

  Raises:
      Exception: Raises an exception if the git clone returns a none zero value
  """
  tldr_cache = os.path.join(wf.cachedir, 'tldr')
  if not os.path.exists(tldr_cache):
    cmd = ['git', 'clone', 'https://github.com/tldr-pages/tldr.git', tldr_cache]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = p.communicate()
    if p.returncode:
      raise Exception(f'Unknown clone error: {stdout}')


def update(days=0):
  tldr_cache = os.path.join(wf.cachedir, 'tldr')
  config_path = os.path.join(wf.datadir, 'config.json')
  if days > 0 and os.path.exists(config_path):
    with open(config_path, encoding='utf-8') as f:
      try:
        config = json.load(f)
      except:
        config = {'update_date': datetime.datetime.now().strftime('%Y%m%d')}

    if (datetime.datetime.now().date() - datetime.datetime.strptime(config['update_date'], '%Y%m%d').date()).days < days:
      return
  os.chdir(tldr_cache)
  local = subprocess.check_output('git rev-parse main'.split()).strip()
  remote = subprocess.check_output(
    'git ls-remote https://github.com/tldr-pages/tldr/ HEAD'.split()
  ).split()[0]

  if local != remote:
    subprocess.check_call('git checkout main'.split())
    subprocess.check_call('git pull --rebase'.split())

  with open(config_path, mode='w') as f:
    data = {
      'update_date': datetime.datetime.now().strftime('%Y%m%d')
    }
    json.dump(data, f)
    wf.cached_data('index', download_index, 1)


def parse_args(query=''):
  query = query.split()
  dic = {
    'isUpdate': False,
    'platform': default_platform,
    'command': ''
  }
  try:
    opts, args = getopt.gnu_getopt(query, 'uo:')
  except:
    return dic

  for opt, arg in opts:
    if opt == '-u':
      dic['isUpdate'] = True
    elif opt == '-o':
      dic['platform'] = arg

  dic['command'] = '-'.join(args)

  return dic


def download_index():
  """Download the tldr index

  Returns:
      dict: The loaded index dictionary
  """
  url = 'http://tldr.sh/assets/index.json'
  response = web.get(url)
  return response.json()

def hint(command, platform=''):
  if (len(command) == 0):
    return []

  index = wf.cached_data('index', download_index, CACHE_TTL * 86400)

  result = []
  for item in index['commands']:
    if (platform in item['platform'] or 'common' in item['platform']) and command == item['name'][0: len(command)]:
      if platform == 'osx':
        autocomplete = item['name']
      elif len(platform) > 0:
        autocomplete = item['name'] + ' -o ' + platform

      result.append({
        'uid': str(time.time()),
        'arg': '',
        'autocomplete': autocomplete,
        'icon': 'icon.png',
        'title': item['name'],
        'valid': 'no'
      })
  return result


def main(wf):
  if wf.update_available:
    wf.start_update()

  if len(wf.args):
    log.debug("HIER")
    query(wf.args[0])
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(update_settings=UPDATE_SETTINGS,
                  help_url=HELP_URL)
    log = wf.logger
    sys.exit(wf.run(main))
