if (window.hljs) {
  window.hljs.highlightAll();
}

const commentsButton = document.getElementById('load-comments');
if (commentsButton) {
  commentsButton.addEventListener('click', () => {
    const status = document.getElementById('comments-status');
    commentsButton.disabled = true;
    status.textContent = 'Loading comments…';

    window.disqus_config = function () {
      this.page.url = commentsButton.dataset.pageUrl;
      this.page.identifier = commentsButton.dataset.pageIdentifier;
      this.callbacks.onReady = [function () {
        status.textContent = '';
        commentsButton.hidden = true;
      }];
    };

    const script = document.createElement('script');
    script.src = 'https://sarbull-github-io.disqus.com/embed.js';
    script.referrerPolicy = 'no-referrer';
    script.onerror = () => {
      status.textContent = 'Comments could not load. Please try again.';
      commentsButton.disabled = false;
      script.remove();
    };
    document.body.appendChild(script);
  });
}
