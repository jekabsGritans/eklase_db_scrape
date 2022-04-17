#FILL VARIABLES AND RENAME TO config.py

# Max http requests per second, when adjusting, take into consideration how many proxies are available to your proxy rotator, as too many requests with a single ip might be blocked
# CONCURRENT_REQUESTS=10

# Proxy that redirects HTTP requests to other proxies. Can be, for example, selfhosted with https://github.com/constverum/ProxyBroker (or use paid proxy providers)
# PROXY_ROTATOR_ENDPOINT="http://rotate:password@1.1.1.1:80"

#POSTGRES DataBase configuration
DB_HOST="localhost"
DB_PORT=5432
DB_NAME="DATABASE1"
DB_USER="USER"
DB_PASSWORD="PASSWORD"