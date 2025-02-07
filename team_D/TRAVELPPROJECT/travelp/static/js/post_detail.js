// 型定義を追加
let currentImageIndex: number = 0;
const images: string[] = [
  {% for image in post.images.all %}
    "{{ image.image.url }}",
  {% endfor %}
];

// メイン画像を切り替える関数
function changeImageFromThumbnail(imageUrl: string): void {
  const mainImage = document.getElementById('main-image') as HTMLImageElement;
  mainImage.src = imageUrl;

  // 現在の画像のインデックスを更新
  currentImageIndex = images.indexOf(imageUrl);
  updateImageCount();
}

// 左右の矢印で画像を切り替える関数
function changeThumbnail(direction: 'prev' | 'next'): void {
  if (direction === 'prev') {
    currentImageIndex = (currentImageIndex > 0) ? currentImageIndex - 1 : images.length - 1;
  } else if (direction === 'next') {
    currentImageIndex = (currentImageIndex < images.length - 1) ? currentImageIndex + 1 : 0;
  }

  const newImageUrl = images[currentImageIndex];
  changeImageFromThumbnail(newImageUrl);
}

// 画像の番号を更新する関数
function updateImageCount(): void {
  const imageCount = document.getElementById('image-count') as HTMLElement;
  imageCount.textContent = (currentImageIndex + 1) + " / " + images.length;

  // 画像番号を表示し、3秒後に非表示にする
  imageCount.style.display = 'block'; // 表示
  setTimeout(function() {
    imageCount.style.display = 'none'; // 3秒後に非表示
  }, 3000);
}

// コメント表示・非表示のトグル
function toggleComments(): void {
  const comments = document.getElementById('comment-list') as HTMLElement;
  const button = document.getElementById('show-all-comments') as HTMLButtonElement;
  const commentItems = comments.querySelectorAll('li');

  // 現在の表示状態をチェック
  const areAllCommentsVisible = Array.from(commentItems).every(item => item.style.display === 'block');

  if (areAllCommentsVisible) {
    // すべてのコメントを非表示にする
    for (let i = 5; i < commentItems.length; i++) {
      commentItems[i].style.display = 'none';
    }
    button.textContent = 'すべてのコメントを表示';
  } else {
    // すべてのコメントを表示する
    for (let i = 5; i < commentItems.length; i++) {
      commentItems[i].style.display = 'block';
    }
    button.textContent = 'すべてのコメントを非表示';
  }
}

// 初期状態では最新の5件だけ表示、5件目以降は非表示
document.addEventListener('DOMContentLoaded', function() {
  // 画像番号の初期表示
  updateImageCount();

  // コメントの初期設定
  const commentList = document.getElementById('comment-list') as HTMLElement;
  const commentItems = commentList.querySelectorAll('li');

  // コメントが5件以上の場合、最新の5件だけ表示、5件目以降を非表示にする
  if (commentItems.length > 5) {
    for (let i = 5; i < commentItems.length; i++) {
      commentItems[i].style.display = 'none';  // 5件目以降を非表示
    }

    // ボタンを表示
    const button = document.getElementById('show-all-comments') as HTMLButtonElement;
    button.style.display = 'inline-block'; // ボタンを表示
    button.textContent = 'すべてのコメントを表示'; // ボタンの初期テキスト
  } else {
    // コメントが5件未満の場合、すべて表示
    const button = document.getElementById('show-all-comments') as HTMLButtonElement;
    button.style.display = 'none'; // ボタンを非表示にする
  }
});

// いいね機能のトグル
interface LikeResponse {
  like_count: number;
  liked: boolean;
}

function toggleLike(): void {
  const likeButton = document.getElementById('like-button') as HTMLButtonElement;
  const likeCount = document.getElementById('like-count') as HTMLElement;

  // AJAXリクエストを送信して、いいねを切り替え
  fetch("{% url 'travelp:post_like' post.pk %}", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': '{{ csrf_token }}',
    },
    body: JSON.stringify({ post_pk: {{ post.pk }} })
  })
  .then(response => response.json())
  .then((data: LikeResponse) => {
    // いいねの数を更新
    likeCount.textContent = data.like_count.toString();

    // ボタンの色を更新
    if (data.liked) {
      likeButton.classList.remove('btn-outline-primary');
      likeButton.classList.add('btn-primary');
      likeButton.innerHTML = '🩷';  // ここでハートを表示
    } else {
      likeButton.classList.remove('btn-primary');
      likeButton.classList.add('btn-outline-primary');
      likeButton.innerHTML = '🤍';  // ここでハートを表示
    }
  })
  .catch(error => console.error('Error:', error));
}
