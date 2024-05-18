const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');

searchButton.addEventListener('click', (e) => {
  e.preventDefault();
  const searchValue = searchInput.value;
  window.location.href = `/tayangan/pencarian?q=${searchValue}`;
});

const selectRange = document.getElementById('range');
  selectRange.addEventListener('select', function () {
    console.log("hi")
    print("hi")
    const selectedRange = selectRange.value;
    window.location.href = `/tayangan/?range=${selectedRange}`;
  });