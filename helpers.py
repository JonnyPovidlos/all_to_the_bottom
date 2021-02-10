def parse_log_file(file_name: str) -> list:
    with open(file_name, 'r') as log_file:
        result = []
        for line in log_file.readlines():
            line = line.split('|')[1].split()
            date = line[0]
            time = line[1]
            ip = line[4]
            url = line[5]
            result.append({
                'date': date,
                'time': ':'.join(time.split(':')[0:2]),
                'ip': ip,
                'url': url.replace('https://', ''),
            })
    return result


def parse_url(url: str) -> list:
    url = [
        u
        for u in url.split('/')
        if u
    ]
    url_list = []
    for idx, u in enumerate(url):
        if idx != len(url) - 1:
            url_list.append({
                'parent': u,
                'cur_url': url[idx + 1]
            })
        else:
            url_list.append({
                'parent': '/',
                'cur_url': url[0]
            })
    result = [url_list[-1]] + url_list[0:len(url_list)-1]
    return result

