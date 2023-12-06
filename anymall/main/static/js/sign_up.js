function validate(val) {
    v1 = document.getElementById("name");
    v2 = document.getElementById("email");
    v3 = document.getElementById("pwd");
    v4 = document.getElementById("pwd_check");
    v5 = document.getElementById("phone");
    v6 = document.getElementById("post_code");
    v7 = document.getElementById("adress");
    v8 = document.getElementById("birth");
    v9 = document.getElementById("male_or_female");


    flag1 = true;
    flag2 = true;
    flag3 = true;
    flag4 = true;
    flag5 = true;
    flag6 = true;
    flag7 = true;
    flag8 = true;
    flag9 = true;


    if(val>=1 || val==0) {
        if(v1.value == "") {
            v1.style.borderColor = "red";
            flag1 = false;
        }
        else {
            v1.style.borderColor = "green";
            flag1 = true;
        }
    }

    if(val>=2 || val==0) {
        if(v2.value == "") {
            v2.style.borderColor = "red";
            flag2 = false;
        }
        else {
            v2.style.borderColor = "green";
            flag2 = true;
        }
    }
    if(val>=3 || val==0) {
        if(v3.value == "") {
            v3.style.borderColor = "red";
            flag3 = false;
        }
        else {
            v3.style.borderColor = "green";
            flag3 = true;
        }
    }
    if(val>=4 || val==0) {
        if(v4.value == "") {
            v4.style.borderColor = "red";
            flag4 = false;
        }
        else {
            v4.style.borderColor = "green";
            flag4 = true;
        }
    }
    if(val>=5 || val==0) {
        if(v5.value == "") {
            v5.style.borderColor = "red";
            flag5 = false;
        }
        else {
            v5.style.borderColor = "green";
            flag5 = true;
        }
    }
    if(val>=6 || val==0) {
        if(v6.value == "") {
            v6.style.borderColor = "red";
            flag6 = false;
        }
        else {
            v6.style.borderColor = "green";
            flag6 = true;
        }
    }
    if(val>=7 || val==0) {
        if(v7.value == "") {
            v7.style.borderColor = "red";
            flag6 = false;
        }
        else {
            v7.style.borderColor = "green";
            flag6 = true;
        }
    }
    if(val>=8 || val==0) {
        if(v8.value == "") {
            v8.style.borderColor = "red";
            flag8 = false;
        }
        else {
            v8.style.borderColor = "green";
            flag8 = true;
        }
    }
    if(val>=9 || val==0) {
        if(v9.value == "") {
            v9.style.borderColor = "red";
            flag9 = false;
        }
        else {
            v9.style.borderColor = "green";
            flag9 = true;
        }
    }

    flag = flag1 && flag2 && flag3 && flag4 && flag5 && flag6 && flag7 && flag8 && flag9;

    return flag;
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


