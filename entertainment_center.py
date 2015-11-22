import media
import fresh_tomatoes
import urllib
import json

def retrieve_movie_info(movie_list):
  '''Retrieve movie meta data to instantiate a Movie.

  Retrieves meta data for a movie using the omdb API. The json response
  is used to create a Movie instance, and the instance is appended to
  a list.

  Args:
    movie_list : a list of movie titles with youtube trailer urls

  Returns:
    An array of Movie instances
  '''

  # The list of Movie instances
  favorite_movies = []
  
  for movie in movie_list:
      # Call omdb API for specific movie meta data
      connection = urllib.urlopen('http://www.omdbapi.com/?t='+movie['title']+'&tomatoes=true')
      output = json.loads(connection.read())
      # Pass the json response to our Movie class and append to favorites list
      movie_meta = media.Movie(output, movie['youtube_url'])
      favorite_movies.append(movie_meta)
  connection.close();
  return favorite_movies;


movie_list = [{"title":"Mad Max Fury Road","youtube_url":"https://www.youtube.com/watch?v=hEJnMQG9ev8"},
              {"title":"Avengers: Age of Ultron","youtube_url":"https://www.youtube.com/watch?v=rD8lWtcgeyg"},
              {"title":"Inside Out","youtube_url":"https://www.youtube.com/watch?v=7ZLOYXKmIkw"},
              {"title":"Jurassic World","youtube_url":"https://www.youtube.com/watch?v=aJJrkyHas78"},
              {"title":"Ex Machina","youtube_url":"https://www.youtube.com/watch?v=gyKqHOgMi4g"},
              {"title":"Terminator Genisys","youtube_url":"https://www.youtube.com/watch?v=62E4FJTwSuc"}]


fresh_tomatoes.open_movies_page(retrieve_movie_info(movie_list))
