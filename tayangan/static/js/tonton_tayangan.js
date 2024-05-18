const progressInput = document.getElementById('progress-input');
const progressValue = document.getElementById('progress-value');

progressInput.addEventListener('input', () => {
  progressValue.innerHTML = progressInput.value;
});

const tontonButton = document.getElementById('tonton-button');

tontonButton.addEventListener('click', async () => {
  const progress = progressInput.value;
  const id_tayangan = document.getElementById('id_tayangan').value;
  console.log(id_tayangan);
  let response = await fetch('/tayangan/tonton', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id_tayangan: id_tayangan,
      progress: parseInt(progress)
    }),
  });
  response = await response.json();
  if (response.status === 'success') {
    alert('BERHASIL menambahkan riwayat menonton tayangan');
    window.location.reload();
  } else {
    alert('GAGAL menambahkan riwayat menonton tayangan');
  }
});