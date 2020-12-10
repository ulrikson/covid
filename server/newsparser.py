import requests

def getFeed():
    response = requests.get('https://www.inoreader.com/stream/user/1004561045/tag/COVID-19%20Sweden/view/json')
    data = response.json()
    return data['items']

def getNewsPosts():
    feed = getFeed()

    newsposts = []
    titles = []

    for item in feed:
        title = item["title"].strip().replace(u'\xa0', u' ')

        # checking so that identical not already exists
        if title not in titles:
            titles.append(title)
            newsposts.append({
                'title': title,
                'url': item['url']
            })

    return {
        'posts': newsposts
    }