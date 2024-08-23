function showMorePosts() {
    var pageCur = Number(document.getElementById("page-cur").value);
    var pageNum = Number(document.getElementById("page-num").value);
    pageCur += 1;
    
    fetch('?page=' + pageCur, {
    headers: {
        'X-Requested-With': 'XMLHttpRequest'
    }
    })
    .then(response => {
        console.log(response);

    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }

    return response.text();
    })
    .then(data => {
        document.getElementsByClassName("feed-container")[0].innerHTML += data;
        document.getElementById("page-cur").value = pageCur;
        if (pageCur == pageNum) {
            document.getElementById("show-more-posts").style.display = "none";
        }
    })
    .catch(error => console.log('Error:', error));
}