// ページロード後に自動リダイレクトする機能
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
      window.location.href = 'search.html'; // 3秒後にsearch.htmlへリダイレクト
  }, 3000); // 3000ミリ秒 = 3秒
});