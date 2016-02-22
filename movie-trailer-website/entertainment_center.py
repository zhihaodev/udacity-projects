#!/usr/bin/env python

"""Create Movie instances, and generate corresponding movie trailer website."""

import media
import fresh_tomatoes

# Create Movie instances
the_grandmaster = media.Movie(
  "The Grandmaster",
  "http://ia.media-imdb.com/images/M/MV5BMTQ0OTY2NTU2MF5BMl5BanBnXkFtZTcwNTEyMjY2OQ@@._V1_SX214_AL_.jpg",  # noqa
  "https://www.youtube.com/watch?v=uC5amKLgnFU",
  "The story of martial-arts master Ip Man, the man who trained Bruce Lee.")
the_continent = media.Movie(
  "The Continent",
  "http://ia.media-imdb.com/images/M/MV5BMTEwMzMzNDc3MDNeQTJeQWpwZ15BbWU4MDg4Mzg5MjIx._V1_SY317_CR51,0,214,317_AL_.jpg",  # noqa
  "https://www.youtube.com/watch?v=oKXpZN0nzW8",
  ("Three men go on a road trip to find a new life "
  "away from the island they live on."))

ted = media.Movie(
  "Ted 2",
  "http://ia.media-imdb.com/images/M/MV5BMjEwMDg3MDk1NF5BMl5BanBnXkFtZTgwNjYyODA1NTE@._V1_SX214_AL_.jpg",  # noqa
  "https://www.youtube.com/watch?v=S3AVcCggRnU",
  ("Newlywed couple Ted and Tami-Lynn want to have a baby, "
  "but in order to qualify to be a parent, "
  "Ted will have to prove he's a person in a court of law."))
jurassic_world = media.Movie(
  "Jurassic World",
  "http://ia.media-imdb.com/images/M/MV5BMTQ5MTE0MTk3Nl5BMl5BanBnXkFtZTgwMjczMzk2NTE@._V1_SX214_AL_.jpg",  # noqa
  "https://www.youtube.com/watch?v=RFinNxS5KN4",
  ("A new theme park is built on the original site of Jurassic Park. "
  "Everything is going well until the park's newest attraction"
  "--a genetically modified giant stealth killing machine"
  "--escapes containment and goes on a killing spree."))
kingsman = media.Movie(
  "Kingsman: The Secret Service",
  "http://ia.media-imdb.com/images/M/MV5BMTkxMjgwMDM4Ml5BMl5BanBnXkFtZTgwMTk3NTIwNDE@._V1_SY317_CR0,0,214,317_AL_.jpg",  # noqa
  "https://www.youtube.com/watch?v=kl8F-8tR8to",
  ("A spy organization recruits an unrefined, "
  "but promising street kid into the agency's "
  "ultra-competitive training program, "
  "just as a global threat emerges from a twisted tech genius."))
the_imitation_game = media.Movie(
  "The Imitation Game",
  "http://ia.media-imdb.com/images/M/MV5BNDkwNTEyMzkzNl5BMl5BanBnXkFtZTgwNTAwNzk3MjE@._V1_SY317_CR0,0,214,317_AL_.jpg",  # noqa
  "https://www.youtube.com/watch?v=S5CjKEFb-sM",
  ("During World War II, mathematician Alan Turing tries to "
  "crack the enigma code with help from fellow mathematicians."))

# Construct a list of movies
movies = [the_grandmaster, the_continent, ted,
          jurassic_world, kingsman, the_imitation_game]

# Generate and open the resulting movie trailer website
fresh_tomatoes.open_movies_page(movies)
