console.log("Script loaded successfully.");

const panel = document.getElementById('profile-panel');

function toggleProfile(event) {
  event.stopPropagation(); // VERY IMPORTANT
  panel.classList.toggle('open');
}

// close when clicking anywhere else
document.addEventListener('click', function () {
  panel.classList.remove('open');
});