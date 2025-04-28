import requests

url = 'https://eqn.hsc.gov.ua/api/v2/departments'
params = {
    'serviceId': '49',
    'date': '2025-05-10'
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,uk;q=0.5',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
}

cookies = {
    #'ak_bmsc': '49CDB14342EE7846C36F544AFB976C22~000000000000000000000000000000~YAAQbDYQYGUC7D6WAQAAuq6sbBtYu33O1SbQDU20ciCd90mlK4KozLxPxzzVbax0Cg0YRqQTTCyKbnUi78upvbRuEBGfqZ46st5yeaz+J5d+1ROL3P/OlxfM5p6uZSjcyWINGmT4kOz6Ef0CByg+yGaS8nytLrroGMTZZf7xvuysC5nNOhtrJ0KNNZt43ZeFrrbAZfOdL6DS+5qjdA6LLXeJckOzQ65OjwyNYngbpNUzltfKHsFbAiZheLM/d6b+2BUEPaJIwm1IQohU/jg2MVEhfoHLINzLKKMXcPYLD3cnzF3qDGDpSLtL6VNHCGIw+0aIUlsPr7Q2z0Lmx497fszNDqSkPcYccEjH8I+uESxGX0WEMZI4Tz1ELWp8mbCmRXo+iFKFRUtKDd4=',
    '__Secure-next-auth.session-token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7ImlubiI6IjI4MjM2MTg3MzMiLCJwaG9uZSI6IiIsImVtYWlsIjoiIiwiZ2l2ZW5uYW1lIjoi0JLQntCb0J7QlNCY0JzQmNCgIiwibWlkZGxlbmFtZSI6ItCb0JXQntCd0IbQlNCe0JLQmNCnIiwibGFzdG5hbWUiOiLQn9Ce0J_QntCSIiwib3JnYW5pemF0aW9uIjoi0KTQhtCX0JjQp9Cd0JAg0J7QodCe0JHQkCIsImVkcnBvdSI6IiJ9LCJleHAiOjE3NDU1ODcyMDguODA2LCJpYXQiOjE3NDU1ODAwMDl9.R0HDTQ7zKSAHQtFgJS_M9IMEwxR8_K6p571nV36SYwUqje6uIOEgN_gPLkWpmwppF94fqlRQO0DhCrh_9FGFvBQ_MTr6pZlmwWldvtd1UXMILgj-eqJSiRUloipW2UgfDaYFEKCAvf38On2zrZq_o0J4AuhEADdRqdLDy02vjMJyYOGVUMImQ7sDRRgjMaEFTX8pkpFUtjp6aOVYZouUPmoZXNs96dvjM1TmGTbFivLA1qgPRFUqOqNe5jIvrPYYxmJ_bQ-y7DrSBidgKncRTqCLDADx-vEs1uxpld_drHP_DH42eTCjcCY5LlDoK3cqZeN7N65W2UEgEWAgDLtmfA',
    #'bm_mi': '3DFF316C2848FF9A3D253317BB24C03B~YAAQbDYQYBxe7D6WAQAAFfS1bBv6LveTkzQdmWzA9EduCkLUP9limepKl0MivmC5QJCzNRLF53osRcm+g6ZkZsKVoNgw2xWCksdOuOi7Qoh/vrfRc/sgwNr6vI7ujs4tyReOlbzXkaf5SCDR6Fq7AE/YXlf9QDyiEGZLInmfjYyuQt+73prd4id+CRkhX7QIGZG1vgUFzdT2AI9MX5LXsLUOhyQHszqPIWsduJSLQ5zKyD6Pf+TbHhZiNzOXUUw8iCT67PpIS30DJgaEK1+19Lpb2FS2YX7VVb2JYBS1HTpAt/Ni25zHU8bWksrX2Wl7+6L1+go=~1',
    #'bm_sv': '60853D1F2B17129F07CF3C94CDD5B8A1~YAAQbDYQYNNf7D6WAQAAIiG2bBsTJ5/Uf2vVXd7ZS4DiwKufBv4WppcCwT/58z0BZNsyC6pwGoSVdL7dSN9Q4IVs17wgmop4IP6E5nN5kq7pEJtQPr/nd5qEbO1wmpGgzaCuJwlXZd+0HYxrVnGRv12/qJtmb+KQPUMfd4KzBw5LtgrEsad3/zXGie6k1gkSNGb1YcCaZUJOwNnbch1X0I4k4jKra9i71WR1OSHYoXB2Cs3MTZl+K2udbqtEP3sOlA==~1'
}

response = requests.get(url, params=params, headers=headers, cookies=cookies)

# Print the status code
print(f"Status Code: {response.status_code}")

# Print the response content
print("Response Content:")
print(response.text)