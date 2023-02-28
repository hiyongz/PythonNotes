import logging

try:
  res = 1 / 0
except Exception as e:
  # logging.error(e, exc_info=True)
  logging.exception(e)

