
const hamburger = document.getElementById("hamburger");
const navMenu = document.getElementById("navMenu");
const pages = document.querySelectorAll(".page");
const navLinks = document.querySelectorAll(".nav-link");
const trendingContainer = document.getElementById("trendingTracks");
const artistsContainer = document.getElementById("artistsList");
const searchBtn = document.getElementById("searchBtn");
const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");

// Hamburger toggle
hamburger.addEventListener("click", () => {
  navMenu.classList.toggle("show");
});

// Page navigation
navLinks.forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    const page = e.target.dataset.page;
    pages.forEach(p => p.classList.remove("active"));
    document.getElementById(page).classList.add("active");
    navMenu.classList.remove("show");

    if(page === "home") fetchTrending();
    if(page === "artists") fetchArtists();
  });
});

// Fetch Trending Tracks
async function fetchTrending() {
  trendingContainer.innerHTML = "Loading...";
  try {
    const res = await fetch("/api/audius?type=trending");
    const data = await res.json();
    trendingContainer.innerHTML = "";
    data.data.forEach(track => {
      const div = document.createElement("div");
      div.className = "track";
      div.innerHTML = `
        <img src="${track.cover_art || 'https://via.placeholder.com/150'}" alt="${track.title}">
        <div class="title">${track.title}</div>
        <div class="artist">${track.user.name}</div>
      `;
      div.addEventListener("click", () => playTrack(track));
      trendingContainer.appendChild(div);
    });
  } catch(err) {
    trendingContainer.innerHTML = "Failed to load tracks.";
    console.error("Error fetching Audius trending:", err);
  }
}

// Fetch Artists
async function fetchArtists() {
  artistsContainer.innerHTML = "Loading...";
  try {
    const res = await fetch("/api/audius?type=artists");
    const data = await res.json();
    artistsContainer.innerHTML = "";
    data.data.forEach(artist => {
      const div = document.createElement("div");
      div.className = "track";
      div.innerHTML = `
        <img src="${artist.profile_picture || 'https://via.placeholder.com/150'}" alt="${artist.name}">
        <div class="title">${artist.name}</div>
        <div class="artist">${artist.followers_count} Followers</div>
      `;
      artistsContainer.appendChild(div);
    });
  } catch(err) {
    artistsContainer.innerHTML = "Failed to load artists.";
    console.error("Error fetching Audius artists:", err);
  }
}

// Search
searchBtn.addEventListener("click", async () => {
  const query = searchInput.value.trim();
  if(!query) return;
  searchResults.innerHTML = "Searching...";
  try {
    const res = await fetch(`/api/audius?type=search&query=${encodeURIComponent(query)}`);
    const data = await res.json();
    searchResults.innerHTML = "";
    data.data.forEach(track => {
      const div = document.createElement("div");
      div.className = "track";
      div.innerHTML = `
        <img src="${track.cover_art || 'https://via.placeholder.com/150'}" alt="${track.title}">
        <div class="title">${track.title}</div>
        <div class="artist">${track.user.name}</div>
      `;
      div.addEventListener("click", () => playTrack(track));
      searchResults.appendChild(div);
    });
  } catch(err) {
    searchResults.innerHTML = "Search failed.";
    console.error("Error searching Audius:", err);
  }
});

// Player
const musicPlayer = document.getElementById("musicPlayer");
const trackThumb = document.getElementById("trackThumb");
const trackTitle = document.getElementById("trackTitle");
const trackArtist = document.getElementById("trackArtist");
const playPauseBtn = document.getElementById("playPause");
const closePlayer = document.getElementById("closePlayer");
let audio = new Audio();
let isPlaying = false;

function playTrack(track) {
  audio.src = track.preview_url || track.audio || track.download?.url; // fallback
  trackThumb.src = track.cover_art || 'https://via.placeholder.com/150';
  trackTitle.textContent = track.title;
  trackArtist.textContent = track.user.name;
  musicPlayer.classList.add("show");
  audio.play();
  isPlaying = true;
  playPauseBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
}

playPauseBtn.addEventListener("click", () => {
  if(isPlaying) {
    audio.pause();
    playPauseBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
  } else {
    audio.play();
    playPauseBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
  }
  isPlaying = !isPlaying;
});

closePlayer.addEventListener("click", () => {
  audio.pause();
  isPlaying = false;
  musicPlayer.classList.remove("show");
});

// Initial load
fetchTrending();