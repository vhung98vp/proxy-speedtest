from src.main import test_all_proxies
import re

results = test_all_proxies()
ip_count = sum(map(lambda x: 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', x['ip']) else 0, results))
speed_count = sum(map(lambda x: 1 if x['speed_result']['download_speed'] != 'N/A' else 0, results))
search_count = sum(map(lambda x: 1 if x['first_url'] else 0, results))

print(results)
print(f'Invalid records total: {len(results) - ip_count} IPs, {len(results) - speed_count} download_speeds, {len(results) - search_count} urls')