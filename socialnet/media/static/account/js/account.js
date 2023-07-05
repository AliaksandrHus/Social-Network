
document.addEventListener("DOMContentLoaded", function(event) {
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, scrollpos);
});

window.onbeforeunload = function(e) {
    localStorage.setItem('scrollpos', window.scrollY);
};




window.addEventListener('load', function() {
    const submitBtn = document.querySelector('#submitBtn');

    if (submitBtn) { // проверяем, существует ли элемент на странице
        window.addEventListener('scroll', function() {
            if (window.scrollY === 0) { // используем window.scrollY вместо window.pageYOffset
                submitBtn.click();
            }
        });
    }
});


