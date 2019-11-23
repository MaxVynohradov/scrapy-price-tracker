# from proxyscrape import create_collector
#
#
# collector = create_collector('default', 'http')
# proxy = collector.get_proxy({'code': ('ua', 'ru', 'by'), 'anonymous': True})
#
# print(proxy)

from proxyscrape import get_proxyscrape_resource
resource_name = get_proxyscrape_resource(proxytype='http', timeout=5000, ssl='yes', anonymity='all', country='us')
