const submitUlasanButton = document.getElementById('submit-ulasan-button');
submitUlasanButton.addEventListener('click', async () => {
  const rating = document.getElementById('ulasan-rating-input').value;
  const deskripsi = document.getElementById('ulasan-deskripsi-input').value;
  const id_tayangan = document.getElementById('id_tayangan').value;

  const response = await fetch('/ulasan/create/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      rating,
      deskripsi,
      id_tayangan,
    }),
  });

  if (response.ok) {
    alert('Ulasan berhasil ditambahkan');
    window.location.reload();
  } else {
    alert('Gagal menambahkan ulasan');
  }
});