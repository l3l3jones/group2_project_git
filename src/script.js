
//loads the main page with a call to app.py endpoint, returning movies now playing in cinema
//uses displayMovies function to add a div for each movie returned to the movie grid
document.addEventListener("DOMContentLoaded", function(){
    fetch('http://127.0.0.1:5000/loading_page')
//asynchronous task, waiting for API call to return results
    .then(response => response.json())
    .then(movies => {
        displayMovies(movies);
    })
//error handling
    .catch(error => console.error('Error getting movies:', error));
});

//function to populate the genre dropdown, fetching the genres from app.py /genres endpoint

function loadGenres() {
    fetch('http://127.0.0.1:5000/genres')
    .then(response => response.json())
    .then(data => {
        const genres = data.genres;
//        creates one option for each genre and appends to dropdown; value is genre id and text showing is the genre name
        const genreDropdown = document.getElementById('genreDropdown');
        //for all Genres, the value is empty string
        genreDropdown.innerHTML = '<option value="">All Genres</option>';
        genres.forEach(genre => {
            genreDropdown.innerHTML += `<option value="${genre.id}">${genre.name}</option>`;
        });
    });
}

//calling the function to load the genres
loadGenres();

//function to display the movies; reworks the data received and adds one div for each movie
function displayMovies(movies) {
//retrieving the movieGrid div element
    let movieGrid = document.getElementById('movieGrid');
// emptying the previous content
    document.getElementById('movieGrid').innerHTML = '';
// looping through data and creating a div element for each movie
    movies.forEach(movie => {
        let movie_div = document.createElement('div');
        movie_div.className = 'movie';
// creating the poster img and appending it to movie_div
        let poster = document.createElement('img');
        poster.src = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
        poster.alt = `${movie.title} Movie`;
        movie_div.appendChild(poster);
//creating the title element h3 and appending to movie_div
        let title = document.createElement('h3');
        title.textContent = movie.title;
        movie_div.appendChild(title);
//creating the overview paragraph element and appending to movie_div
        let overview = document.createElement('p');
        overview.innerText = movie.overview;
        movie_div.appendChild(overview);
// class created so we can modify the overview
        overview.className = 'overview';
// creating the rating p element
        let rating = document.createElement('p');
// will show 'No reviews yet' if rating is 0
        if (movie.vote_average == 0){
        rating.textContent = 'No reviews yet'
        } else {
//rating modified to show only one decimal
        rating.textContent = `Rating: ${movie.vote_average.toFixed(1)}/10`;
        }
        movie_div.appendChild(rating);
// appending each movie_div to the main container
        movieGrid.appendChild(movie_div);
    });
}

// function that sends fetch requests to back end
function searchMovies() {
// getting the values of the fields after Search button is clicked/ enter pressed
    let query = document.getElementById('search-bar').value;
    let decade = document.getElementById('decadeDropdown').value;
    let genre = document.getElementById('genreDropdown').value;
// checking if the checkbox for movies playing in the cinema at the moment is clicked
    const isNowPlayingChecked = document.getElementById('nowPlayingCheckbox').checked;
// creating route variable which will contain the endpoint we want to call
//depending if now playing is ticked or there is a query word
    let route = '';
//if query is not empty, so there is a keyword

    if (query != '') {
// checking with ternary operator what the endpoint should be, depending on now playing ticked or not
     route = isNowPlayingChecked
                    ? 'http://127.0.0.1:5000/movies/now_playing_search'
                    : 'http://127.0.0.1:5000/movies/search';
     } else {
// if no keyword is specified, the endpoint will be different; this search does not differentiate between movies in cinema or not
        route = 'http://127.0.0.1:5000/movies/genre';
     }

// emptying the movie grid of previous movies
    document.getElementById('movieGrid').innerHTML = '';
// sending fetch request wih the 3 variables query, decade & genre; if any is not supplied, they default to empty string
    fetch(`${route}?query=${query}&decade=${decade}&genre=${genre}`)
//asynchronous task, waiting for API call to return response
    .then(response => response.json())
    .then(data => {
        console.log(data);
        displayMovies(data);
    })
//    error handling
    .catch(error => {
        console.error('Error fetching movies:', error);
    });
}

// extra event listener so the search works when enter key is pressed, not only when clicking the search button
document.getElementById('search-bar').addEventListener('keyup', function(event) {
// calls searchMovies function
    if (event.key === 'Enter') {
        searchMovies();
    }
});



