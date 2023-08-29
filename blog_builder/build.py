import json
import time
import datetime
import re
import sys

def get_title(output_file):
    with open(output_file, 'r') as f:
        html = f.read()
        title = re.search(r'<title>(.*)</title>', html).group(1)
        return title

def get_date(output_file):
    with open(output_file, 'r') as f:
        html = f.read()
        date = re.search(r"<div class=\"date\"> Date:  (.*) </div>", html).group(1)
        return date

def add_tweet_button(output_file):
    BUTTON = """
<a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-show-count="false">Tweet</a>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
"""
    with open(output_file, 'r') as f:
        html = f.read()
        html = html.replace('</body>', BUTTON + '</body>')
    with open(output_file, 'w') as f:
        f.write(html)


def build_article(out_file):
    date = get_date(out_file)
    title = get_title(out_file)
    add_tweet_button(out_file)
    output_file = out_file.replace('../public/', '')
    with open('../public/posts.json', 'r') as f:
        posts = json.load(f)
        for post in posts:
            if post['title'] == title:
                updated_post = {
                    'title': title,
                    'post_date': date,
                    'url': output_file
                }
                posts.remove(post)
                posts.append(updated_post)
                break
        else:
            posts.append({
                'title': title,
                'post_date': date,
                'url': output_file
            })

        
    with open('../public/posts.json', 'w') as f:
        json.dump(posts, f)

    posts = sorted(posts, key=lambda x: time.strptime(x['post_date'], '%Y/%m/%d'), reverse=True)

    recent_posts = posts[:5]
    with open('../public/recent_posts.json', 'w') as f:
        json.dump(recent_posts, f)

    

if __name__ == '__main__':
    output_file = sys.argv[1]
    build_article(output_file)
