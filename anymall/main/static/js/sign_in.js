// login_email.js

// 페이지 로드가 완료된 후 실행될 함수
document.addEventListener("DOMContentLoaded", function () {
    // Sign Up 버튼에 클릭 이벤트 핸들러 추가
    var logInButton = document.querySelector(".btn-primary");
    if (logInButton) {
        logInButton.addEventListener("click", function () {
            redirectToSignUp();
        });
    }
});

// login_email 페이지로 이동하는 함수
function redirectToSignUp() {
    window.location.href = "/sign_up"; // 원하는 URL로 변경하세요.
}

// X누르면 홈화면으로
document.addEventListener("DOMContentLoaded", function () {
    // "fa-times" 아이콘을 찾습니다.
    var closeButton = document.querySelector(".fas.fa-times");

    // "fa-times" 아이콘이 클릭되면 이벤트 핸들러를 실행합니다.
    if (closeButton) {
        closeButton.addEventListener("click", function () {
            // 인덱스 페이지로 이동합니다.
            window.location.href = "/"; // 원하는 URL로 변경하세요.
        });
    }
});