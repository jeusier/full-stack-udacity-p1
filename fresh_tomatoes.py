import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
       body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
        }
        .movie-tile .left-content {
          float: left;
          cursor: pointer;
        }
        .movie-tile .left-content .movie-image:hover {
          box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
        }
        .movie-tile .right-content {
          padding-left:230px;
        }
        .movie-tile .ratings-box {
          margin-left: 10px;
          padding: 10px;
        }
        .movie-tile .rating {
          float: left;
          width: 50%;
          margin-bottom:10px;
        }
        .movie-tile .score {
          display: block;
          font-size:24px;
          font-weight:bold;
        }
        .movie-tile .critics {
          margin-top:20px;
        }
        .movie-tile .critics-text {
          color: #787878;
        }
        .movie-tile .movie-info {
          overflow: hidden;
          max-height: 0;
          transition: max-height .5s ease-in-out;
        }
        .movie-tile:hover .movie-info {
          max-height: 400px;
          transition: max-height .5s ease-in-out;
        }
        .movie-tile .dl-horizontal dd {
          text-align: left;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        @media screen and (max-width: 767px) {
          .movie-tile .left-content {
            float: none;
          }
          .movie-tile .right-content {
            padding: 0;
          }
          .movie-tile .ratings-box {
            margin: 0;
          }
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-image', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-xs-12 col-md-6 movie-tile text-center clearfix">
  <div class="left-content clearfix">
    <img class="movie-image" src="{poster_image_url}" width="220" height="342" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
  </div>
  <div class="right-content clearfix">
    <h2>{movie_title}</h2>
    <div class="ratings-box">
      <div class="rating">
        <span class="rater">Tomatometer</span>
        <span class="score">{movie_tomato_rating}%</span>
      </div>
      <div class="rating">
        <span class="rater">IMDBometer</span>
        <span class="score">{movie_imdb_rating}</span>
      </div>
      <p class="critics"><span class='critics-text'>Critics say:</span> {movie_tomato_consensus}</p>
    </div>
  </div>
  <div class="movie-info">
    <h3>Movie Info</h3>
    <p>{movie_storyline}
    <dl class="dl-horizontal">
      <dt>Rated</dt>
      <dd>{movie_rated}</dd>
      <dt>Release Date</dt>
      <dd>{release_date}</dd>
      <dt>Genre</dt>
      <dd>{movie_genre}</dd>
      <dt>Director</dt>
      <dd>{movie_director}</dd>
      <dt>Actors</dt>
      <dd>{movie_actors}</dd>
    </dl>
  </div>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            release_date=movie.release_date,
            movie_rated=movie.rated,
            movie_genre=movie.genre,
            movie_storyline=movie.storyline,
            movie_tomato_rating=movie.tomato_rating,
            movie_imdb_rating=movie.imdb_rating,
            movie_tomato_consensus=movie.tomato_consensus,
            movie_director=movie.director,
            movie_actors=movie.actors
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
