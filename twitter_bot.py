import tweepy
import os
import random

def create_api():
    """
    Membuat dan mengotentikasi objek API Twitter.
    Mengambil credentials dari GitHub Secrets.
    """
    consumer_key = os.environ.get('TWITTER_API_KEY')
    consumer_secret = os.environ.get('TWITTER_API_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    try:
        api.verify_credentials()
        print("Authentication OK")
    except Exception as e:
        print("Error during authentication")
        raise e
        
    return api

def get_trending_hashtags(api, woeid=1047378):
    """
    Mengambil hashtag yang sedang trending.
    WOEID 1047378 adalah untuk Indonesia. Ganti dengan 1 untuk Worldwide.
    """
    try:
        trends = api.get_place_trends(id=woeid)
        # Ambil hanya hashtags dari trends
        hashtags = [trend['name'] for trend in trends[0]['trends'] if trend['name'].startswith('#')]
        print(f"Berhasil mendapatkan hashtags: {hashtags[:5]}")
        # Ambil 2 hashtag teratas secara acak agar tidak monoton
        return random.sample(hashtags[:5], 2) if len(hashtags) >= 2 else hashtags
    except Exception as e:
        print(f"Gagal mengambil trends: {e}")
        return []

def compose_tweet(hashtags):
    """
    Menyusun teks tweet.
    Anda bisa memodifikasi bagian ini sekreatif mungkin.
    """
    # Contoh daftar konten tweet, bisa link blog, kutipan, dll.
    tweet_contents = [
        "Penasaran dengan teknologi AI terbaru? Cek artikel ini: https://namabloganda.com/artikel-1",
        "Bagaimana cara kerja Machine Learning? Simak penjelasannya di sini: https://namabloganda.com/artikel-2",
        "Contoh Quote Retweet video keren: https://twitter.com/NASA/status/1546892473455910912", # Link ke tweet dengan video
        "Tips produktif untuk para developer di 2025! Kunjungi: https://namabloganda.com/artikel-3"
    ]

    # Pilih satu konten secara acak
    main_content = random.choice(tweet_contents)
    
    # Gabungkan konten dengan hashtags
    hashtag_string = " ".join(hashtags)
    
    # Struktur tweet yang rapi
    full_tweet = f"{main_content}\n\n{hashtag_string}"
    
    # Pastikan tidak melebihi batas karakter Twitter
    return full_tweet[:280]

def main():
    """
    Fungsi utama untuk menjalankan bot.
    """
    api = create_api()
    trending_hashtags = get_trending_hashtags(api, woeid=1047378) # Ganti WOEID jika perlu

    if not trending_hashtags:
        print("Tidak ada hashtag yang didapat, proses dibatalkan.")
        return

    tweet_text = compose_tweet(trending_hashtags)
    
    try:
        client = tweepy.Client(
            consumer_key=os.environ.get('TWITTER_API_KEY'),
            consumer_secret=os.environ.get('TWITTER_API_SECRET'),
            access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        )
        client.create_tweet(text=tweet_text)
        print(f"Tweet berhasil diposting:\n{tweet_text}")
    except Exception as e:
        print(f"Gagal memposting tweet: {e}")

if __name__ == "__main__":
    main()
