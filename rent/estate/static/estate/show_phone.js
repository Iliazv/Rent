function ShowPhone(announcement) {
    document.getElementById("slider__show_" + announcement).style.display = "none";
    document.getElementById("slider__phone_" + announcement).style.display = "block";
}

function ShowSmallPhone() {
    document.getElementById("slider__show_extra").style.display = "none";
    document.getElementById("slider__phone").style.display = "block";
}

function ShowBigPhone() {
    document.getElementById("slider__big_show").style.display = "none";
    document.getElementById("slider__big_phone").style.display = "block";
}