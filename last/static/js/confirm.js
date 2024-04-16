// ページロード後に自動リダイレクトする機能
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
      window.location.href = '/search'; // 3秒後にsearch.htmlへリダイレクト
  }, 10000); // 10000ミリ秒 = 10秒
});