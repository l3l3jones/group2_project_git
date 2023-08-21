
document.addEventListener("DOMContentLoaded", function(){
    fetch('http://127.0.0.1:5000/loading_page')
    .then(response => response.json())
    .then(movies => {
        displayMovies(movies);
    })
    .catch(error => console.error('Error getting movies:', error));
});


function displayMovies(movies) {
    let movieGrid = document.getElementById('movieGrid');
    document.getElementById('movieGrid').innerHTML = '';
    movies.forEach(movie => {
        let movie_div = document.createElement('div');
        movie_div.className = 'movie';

        let poster = document.createElement('img');
        poster.src = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
        poster.alt = `${movie.title} Movie`;
        movie_div.appendChild(poster);

        let title = document.createElement('h3');
        title.textContent = movie.title;
        movie_div.appendChild(title);

        let overview = document.createElement('p');
        overview.innerText = movie.overview.substring(0, 100);
        movie_div.appendChild(overview);
        overview.className = 'overview';

        let rating = document.createElement('p');
        if (movie.vote_average == 0){
        rating.textContent = 'No reviews yet'
        } else {
        rating.textContent = `Rating: ${movie.vote_average.toFixed(1)}/10`;
        }
        movie_div.appendChild(rating);

        movieGrid.appendChild(movie_div);
    });
}

function loadGenres() {
    fetch('http://127.0.0.1:5000/genres')
    .then(response => response.json())
    .then(data => {
        const genres = data.genres;
        const genreDropdown = document.getElementById('genreDropdown');
        genreDropdown.innerHTML = '<option value="">All Genres</option>';
        genres.forEach(genre => {
            genreDropdown.innerHTML += `<option value="${genre.id}">${genre.name}</option>`;
        });
    });
}

loadGenres();

function searchMovies() {
    let query = document.getElementById('search-bar').value;
    let decade = document.getElementById('decadeDropdown').value;
    let genre = document.getElementById('genreDropdown').value;

    const isNowPlayingChecked = document.getElementById('nowPlayingCheckbox').checked;
    let route = '';

    if (query != '') {

     route = isNowPlayingChecked
                    ? 'http://127.0.0.1:5000/movies/now_playing_search'
                    : 'http://127.0.0.1:5000/movies/search';
     } else {
        route = 'http://127.0.0.1:5000/movies/genre';
     }

    document.getElementById('movieGrid').innerHTML = '';

    fetch(`${route}?query=${query}&decade=${decade}&genre=${genre}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        displayMovies(data);
    })
    .catch(error => {
        console.error('Error fetching movies:', error);
    });
}
document.getElementById('search-bar').addEventListener('keyup', function(event) {

    if (event.key === 'Enter') {
        searchMovies();
    }
});



