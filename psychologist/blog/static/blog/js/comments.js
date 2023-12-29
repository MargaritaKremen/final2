document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('submit-comment');
    const commentContent = document.getElementById('comment-content');
    const commentsContainer = document.getElementById('comments-container');
    const likeIcon = document.getElementById('like-icon');
    const likesCountSpan = document.getElementById('likes-count');
    const likeUrl = likeIcon.getAttribute('data-like-url');
    console.log('likeUrl= ', likeUrl)
    // Функция для обновления состояния лайка на основе данных с сервера
    function updateLikeState() {
        fetch(likeUrl)
            .then(response => response.json())
            .then(data => {
                console.log('Data from server:', data);
                console.log('data.likes_count on load=  ', data.likes_count);
                likesCountSpan.textContent = data.likes_count;
                liked = data.liked;
                updateLikeIcon();
            })
            .catch(error => {
                console.error('Error in updateLikeState:', error);
            });
    }
    // Вызываем функцию при загрузке страницы
    updateLikeState();

    // Обработчик события для иконки лайка
    likeIcon.addEventListener('click', function () {
        fetch(likeUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);

                if (data.liked) {
                    likeIcon.classList.remove('fa-regular');
                    likeIcon.classList.add('fa-solid');
                } else {
                    likeIcon.classList.remove('fa-solid');
                    likeIcon.classList.add('fa-regular');
                }
                likesCountSpan.textContent = data.likes_count;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    // Вызываем функцию при загрузке страницы только после нажатия иконки лайка
     likeIcon.addEventListener('click', updateLikeState);



    submitButton.addEventListener('click', function () {
        const content = commentContent.value;

        console.log('Comment Content:', content);

        fetch(addCommentUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },
            body: new URLSearchParams({ 'content': content }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Обновление контейнера с комментариями
                    if (commentsContainer) {
                        const newComment = document.createElement('p');
                        newComment.textContent = `${data.comment.author}: ${data.comment.content}`;
                        commentsContainer.appendChild(newComment);
                    }
                    commentContent.value = '';
                } else {
                    console.error(data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});