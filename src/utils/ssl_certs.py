import os


def configure_ssl_certs() -> None:
  """HTTPS 検証用 CA を設定する（Windows は OS 証明書ストアを優先）。"""
  try:
    import truststore
    truststore.inject_into_ssl()
    return
  except ImportError:
    pass

  try:
    import certifi
  except ImportError:
    return

  ca_bundle = certifi.where()
  os.environ.setdefault("SSL_CERT_FILE", ca_bundle)
  os.environ.setdefault("REQUESTS_CA_BUNDLE", ca_bundle)
