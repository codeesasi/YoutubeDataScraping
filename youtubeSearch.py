from pytubefix import Search

s = Search('YouTube Rewind')

for p in s.videos:
    print(p.title)
    print(p.thumbnail_url)
    print(p.channel_url)
    print(p.views)
    print(p.description)
    print()