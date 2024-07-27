document.addEventListener('DOMContentLoaded', function() {
    var modalPost = document.getElementById('postModal');
    var span = document.getElementsByClassName('close')[0];
    var modalImage = document.getElementById('modalImage');
    var modalUsername = document.getElementsByClassName('modalUsername')[0];
    var posttId = document.getElementById('postId');
    var userId = document.getElementById('userId');
    var postIdCom = document.getElementById('postIdCom');
    var userIdCom = document.getElementById('userIdCom');
    var userAvatar = document.getElementById('modalUserAvatar');
    var postCreatedAt = document.getElementById('postCreatedAt');

    window.imgDetail = function(postId) {
        fetch(`/get_model_data/${postId}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('comment-list').innerHTML = '';
                modalImage.src = data.content;
                modalUsername.innerText = data.user;
                posttId.value = data.id;
                userId.value = data.user_id;
                postIdCom.value = data.id;
                userIdCom.value = data.user_id;
                userAvatar.src = data.user_avatar;
                let createdDate = new Date(data.created_at);
                let formattedDate = createdDate.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: 'numeric',
                    minute: 'numeric',
                    second: 'numeric'
                });
                postCreatedAt.innerText = 'ㅤ' + formattedDate;
                
                if (data.description) {
                    document.getElementById('comment-list').innerHTML += `
                        <div class="comment">
                            <div class="user-avatar">
                                <img src="${data.user_avatar}" alt="">
                            </div>
                            <div class="comment-content">
                                <p class="comment-author">${data.user}</p>
                                <p id="modalDescription">${data.description}</p>
                            </div>
                        </div>
                    `;
                } else if (!data.comments) {
                    document.getElementById('comment-list').innerHTML = '';
                }

                if (data.comments) {
                    data.comments.forEach(comment => {
                        let createdDate = new Date(comment.created_at);
                        let formattedDate = createdDate.toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            hour: 'numeric',
                            minute: 'numeric',
                            second: 'numeric'
                        });
                        document.getElementById('comment-list').innerHTML += `
                            <div class="comment">
                                <div class="user-avatar">
                                    <img src="${comment.user_avatar}" alt="">
                                </div>
                                <div class="comment-content">
                                    <p class="comment-author">${comment.username}</p>
                                    <p id="modalDescription">${comment.content}</p>
                                    <p class="comment-timestamp">${formattedDate}</p>
                                </div>
                            </div>
                        `;
                    });
                } else {
                    document.getElementById('comment-list').innerHTML = '';
                }

                if (data.is_liked) {
                    document.getElementById('likeButton').innerHTML = '<i class="fas fa-heart"></i>' + data.likes_count;
                } else {
                    document.getElementById('likeButton').innerHTML = '<i class="far fa-heart"></i>' + data.likes_count;
                }
                modalPost.style.display = 'block';
            })
            .catch(error => console.error('Error fetching data:', error));
    };

    span.onclick = function() {
        modalPost.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == modalPost) {
            modalPost.style.display = 'none';
        }
    };
});
