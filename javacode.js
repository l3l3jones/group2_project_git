const words1 = ['Horror', 'Action', 'Romance', 'Comedy', 'Thriller'];
const words2 = ['Kids', 'PG/U', '12A', '12', '18'];
const words3 = ['> 1 Hour', '1 - 2 Hours', '2 - 3 Hours', '3 + Hours'];

const spinner1 = document.getElementById('spinner1');
const spinner2 = document.getElementById('spinner2');
const spinner3 = document.getElementById('spinner3');
const selectedResult = document.getElementById('selectedResult');

function populateSpinner(spinner, words) {
  words.forEach(word => {
    const option = document.createElement('option');
    option.value = word;
    option.textContent = word;
    spinner.appendChild(option);
  });
}

populateSpinner(spinner1, words1);
populateSpinner(spinner2, words2);
populateSpinner(spinner3, words3);

spinner1.addEventListener('change', updateResult);
spinner2.addEventListener('change', updateResult);
spinner3.addEventListener('change', updateResult);

function updateResult() {
  const selectedWord1 = spinner1.value;
  const selectedWord2 = spinner2.value;
  const selectedWord3 = spinner3.value;

  selectedResult.textContent = `Selected Words: ${selectedWord1}, ${selectedWord2}, ${selectedWord3}`;
}
