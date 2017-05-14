import scrapy


class OVOSoundSpider(scrapy.Spider):
  name = "ovosound"
  start_urls = [
    'https://genius.com/albums/Drake/Ovo-sound-radio-tracklists'
  ]

  songs = set()

  def parse(self, response):

    for episode in response.css(".song_list a::attr(href)").extract():
      yield scrapy.Request(episode, callback=self.parse_episode)

  def parse_episode(self, response):

    # use song links as a proxy for uniqueness
    songs = response.css(".lyrics > p > a").extract()
    [self.songs.add(song.encode("ascii", "replace")) for song in songs]

    yield {"songs": songs}

  def closed(self, reason):
    # parse stats

    tot = len(self.songs)
    drake = [song for song in self.songs if "drake" in str.lower(song)]


    print "Total songs: {}".format(tot)
    print "Drake songs: {}".format(len(drake))
    print "Overall % of Drake songs {}".format(float(tot) / len(drake))

    print "== All Drake Songs =="
    for s in drake:
      print scrapy.Selector(text=s).xpath('//a/text()').extract()