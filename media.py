class Movie():
  ''' Holds various information about a movie

  Attributes:
    title: A string of the movie title
    storyline: A string for the movie plot
    poster_image: A string for the poster url
    rated: A string for the movie MPAA rating
    release_date: A string for the movie release date
    genre: A string for the movie genre
    trailer_youtube_url: A string for the youtube trailer url
    tomato_rating: A string for the movie Rotten Tomato rating
    imdb_rating: A string for the movie IMDB rating
    tomator_consensus: A string for the movie critic consensus
    director: A string for the movie director
    actors: A string for the movie actors
  '''
  
  def __init__(self, movie, youtube_url):
    self.title = movie['Title']
    self.storyline = movie['Plot']
    self.poster_image_url = movie['Poster']
    self.rated = movie['Rated']
    self.release_date = movie['Released']
    self.genre = movie['Genre']
    self.trailer_youtube_url = youtube_url
    self.tomato_rating = movie['tomatoMeter']
    self.imdb_rating = movie['imdbRating']
    self.tomato_consensus = movie['tomatoConsensus']
    self.director = movie['Director']
    self.actors = movie['Actors']
            
