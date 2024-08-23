const chooseFile = document.getElementById("avatar");
const imgPreview = document.getElementById("pic");

chooseFile.addEventListener("change", function () {
    getImgData();
});

function getImgData() {
const files = chooseFile.files[0];
if (files) {
    const fileReader = new FileReader();
fileReader.readAsDataURL(files);
fileReader.addEventListener("load", function () {
    imgPreview.style.display = "block";
    imgPreview.src = this.result;
});    
}
}