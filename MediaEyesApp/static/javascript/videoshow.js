
/*
function shfaqVideo() {
  var link = document.getElementById('youtube-link').value;

  // Regex për lidhje të plota dhe të shkurtuara YouTube
  var youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/(?:watch\?v=|v\/|e\/|embed\/|shorts\/))([a-zA-Z0-9_-]{11})/;
  var youtubeShortsRegex = /^(https?:\/\/)?(www\.)?(youtu\.be\/)([a-zA-Z0-9_-]{11})/;
  var youtubeShortLinkRegex = /^(https?:\/\/)?(www\.)?(youtu\.be\/)([a-zA-Z0-9_-]{11})(\?si=[a-zA-Z0-9_-]+)?$/; // Përfshin gjithashtu ?si= parametrin

  var match = link.match(youtubeRegex);
  var matchShort = link.match(youtubeShortsRegex);
  var matchShortLink = link.match(youtubeShortLinkRegex);

  // Kontrollo nëse lidhja është valide
  if (match || matchShort || matchShortLink) {
      var videoId = (match) ? match[4] : (matchShort) ? matchShort[4] : matchShortLink[4];  // Nxjerr ID-në e videos nga regex
      var iframe = document.createElement('iframe');
      iframe.width = "500";
      iframe.height = "315";
      iframe.src = "https://www.youtube.com/embed/" + videoId;
      iframe.frameBorder = "0";
      iframe.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture";
      iframe.allowFullscreen = true;

      // Shfaq videon
      var videoContainer = document.getElementById('video-container');
      videoContainer.innerHTML = '';  // Pastroje containerin para se të shtohet videoja
      videoContainer.appendChild(iframe);
  } else {
      alert('Ju lutem futni një lidhje të vlefshme nga YouTube!');
  }
}
*/




function shfaqVideo() {
  var link = document.getElementById('youtube-link').value;

  // Regex për lidhje të plota dhe të shkurtuara YouTube
  var youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/(?:watch\?v=|v\/|e\/|embed\/|shorts\/))([a-zA-Z0-9_-]{11})/;
  var youtubeShortsRegex = /^(https?:\/\/)?(www\.)?(youtu\.be\/)([a-zA-Z0-9_-]{11})/;
  var youtubeShortLinkRegex = /^(https?:\/\/)?(www\.)?(youtu\.be\/)([a-zA-Z0-9_-]{11})(\?si=[a-zA-Z0-9_-]+)?$/;

  var match = link.match(youtubeRegex);
  var matchShort = link.match(youtubeShortsRegex);
  var matchShortLink = link.match(youtubeShortLinkRegex);

  // Kontrollo nëse lidhja është valide
  if (match || matchShort || matchShortLink) {
    var videoId = (match) ? match[4] : (matchShort) ? matchShort[4] : matchShortLink[4];
    var iframe = document.createElement('iframe');
    iframe.src = "https://www.youtube.com/embed/" + videoId;
    iframe.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture";
    iframe.allowFullscreen = true;

    // Shfaq videon
    var videoContainer = document.getElementById('video-container');
    videoContainer.innerHTML = ''; // Pastroje containerin para se të shtohet videoja
    videoContainer.appendChild(iframe);
  } else {
    alert('Ju lutem futni një lidhje të vlefshme nga YouTube!');
  }
}
