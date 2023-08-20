
function displayMovies(movies) {
    let movieGrid = document.getElementById('movieGrid');
    document.getElementById('movieGrid').innerHTML = '';
    movies.forEach(movie => {
        let movieDiv = document.createElement('div');
        movieDiv.className = 'movie';


        let poster = document.createElement('img');
        poster.src = `https://image.tmdb.org/t/p/w500${movie.poster_path}`;
        poster.alt = `${movie.title} Poster`;
        movieDiv.appendChild(poster);


        let title = document.createElement('h3');
        title.textContent = movie.title;
        movieDiv.appendChild(title);

        let overview = document.createElement('p');
        overview.innerText = movie.overview.substring(0, 100);
        movieDiv.appendChild(overview);

        let rating = document.createElement('p');
        if (movie.vote_average == 0){
        rating.textContent = 'No reviews yet'
        } else {
        rating.textContent = `Rating: ${movie.vote_average.toFixed(1)}/10`;
        }
        movieDiv.appendChild(rating);


        movieGrid.appendChild(movieDiv);
    });
}
function loadGenres() {
    fetch('http://127.0.0.1:5000/genres')
    .then(response => response.json())
    .then(data => {
        const genres = data.genres;
        const genreDropdown = document.getElementById('genreDropdown');
        genreDropdown.innerHTML = '<option value="">All Genres</option>';  // Default option
        genres.forEach(genre => {
            genreDropdown.innerHTML += `<option value="${genre.id}">${genre.name}</option>`;
        });
    });
}

loadGenres();

document.addEventListener("DOMContentLoaded", function(){
    fetch('http://127.0.0.1:5000/loading_page')
    .then(response => response.json())
    .then(movies => {
        displayMovies(movies);
    })
    .catch(error => console.error('Error fetching movies:', error));
});

function searchMoviesByDecade() {
    let query = document.getElementById('searchBar').value;
    let decade = document.getElementById('decadeDropdown').value;
    let genre = document.getElementById('genreDropdown').value;

    const isNowPlayingChecked = document.getElementById('nowPlayingToggle').checked;
    let endpoint = isNowPlayingChecked
                    ? 'http://127.0.0.1:5000/movies/now_playing_search'
                    : 'http://127.0.0.1:5000/movies/search';


    document.getElementById('movieGrid').innerHTML = '';

    fetch(`${endpoint}?query=${query}&decade=${decade}&genre=${genre}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        displayMovies(data);
    })
    .catch(error => {
        console.error('Error fetching movies:', error);
    });
}
document.getElementById('searchBar').addEventListener('keyup', function(event) {

    if (event.key === 'Enter') {
        searchMoviesByDecade();
    }
});



