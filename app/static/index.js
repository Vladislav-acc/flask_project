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


function answerComments(commentUser){
    let inputComment = document.getElementById(`text`)
    console.log(inputComment.defaultValue)
    inputComment.defaultValue = commentUser+', '
    inputComment.focus();
    console.log(inputComment.value.length)
    inputComment.selectionStart = inputComment.value.length;
    }


/*let btn = document.getElementById("answer");
btn.addEventListener("click", function(commentUser) {
	//Do something here
	console.log('yyy')
}, false);*/
