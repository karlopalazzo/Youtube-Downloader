from pytubefix import YouTube
from pytubefix.cli import on_progress


# Create YouTubeDownloader class
class YouTubeDownloader:
    """
    Simple class for YouTube video downloader. I used pytube library for this class.
    Documentation link: https://pytube.io/en/latest/user/quickstart.html
    """

    def __init__(self, url):
        self.url = url
        self.yt = YouTube(self.url,
                          on_progress_callback=on_progress,
                          on_complete_callback=self.on_complete,
                          use_oauth=False,
                          allow_oauth_cache=True)
        self.stream = None

    def get_video_info(self) -> dict:
        """
        Get video information
        """
        video_info = {
            "title": self.yt.title,
            "author": self.yt.author,
            "length": self.yt.length,
            "streams": self.yt.streams,
            "captions": self.yt.captions
        }
        return video_info

    def show_available_streams(self) -> YouTube.streams:
        """
        Show available streams
        """
        streams = self.yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
        for i, stream in enumerate(streams):
            print(f"{i + 1}: {stream.resolution} - {stream.fps}fps - {stream.filesize // (1024 * 1024)}MB")
        return streams

    def choose_stream(self, stream_number) -> None:
        """
        Choose stream
        """
        streams = self.show_available_streams()
        if 1 <= stream_number <= len(streams):
            self.stream = streams[stream_number - 1]
        else:
            print("Invalid stream number")

    def download_video(self, path="."):
        """
        Download video
        """
        if self.stream:
            print("Downloading...")
            self.stream.download(output_path=path)
        else:
            print("Please choose a stream")

    def on_complete(self, stream, path):
        print(f"Download completed and saved to {path}")


def main():
    url = input("Enter the YouTube video URL: ")
    downloader = YouTubeDownloader(url)
    downloader.get_video_info()

    print(downloader.show_available_streams())
    stream_number = int(input("Choose a stream number: "))
    downloader.choose_stream(stream_number)

    downloader.download_video()


if __name__ == "__main__":
    main()
