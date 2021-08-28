function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/like_post/${postId}`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if (data["liked"] === true) {
            likeButton.className = "fas fa-thumbs-up";
            } else {
            likeButton.className = "far fa-thumbs-up";
            }
        })
        .catch((e) => alert("Can\'t like post!"));
    }

function showComments(postId) {
    let commentButton = document.getElementById(`comments-button-${postId}`)
    let count = document.getElementById(`comments-count-${postId}`)
    let display = count.style.display
    if (commentButton.textContent.startsWith('Посмотреть')){
        commentButton.textContent = 'Скрыть комментарии'
        count.style.display = 'none'
    }else if(commentButton.textContent.startsWith('Скрыть')){
        commentButton.textContent = 'Посмотреть комментарии'
        count.style.display = 'inline'
    }
}

function updateComments(postId){
    const comments = document.getElementById(`comments-${postId}`)
    console.log(comments)

}
