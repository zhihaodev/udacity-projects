class Movie:

    """Represent a movie with title, poster url, trailer url and storyline."""

    def __init__(self, title, poster_image_url, trailer_youtube_url, storyline):  # noqa
        self.title = title
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url
        self.storyline = storyline
