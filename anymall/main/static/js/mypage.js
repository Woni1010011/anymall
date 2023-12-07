// 모달을 여는 함수
function openModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "block";
}

// 모달을 닫는 함수
function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";
}

// 모달 닫기 버튼 핸들러
var closeButtons = document.getElementsByClassName("close");
for (var i = 0; i < closeButtons.length; i++) {
    closeButtons[i].onclick = function() {
        var modal = this.parentElement.parentElement;
        modal.style.display = "none";
    }
}

// 버튼 클릭 이벤트 리스너
document.addEventListener('click', function (e) {
    if (e.target.dataset.toggle === "refundAccountModal") {
        openModal('refundAccountModal');
    } else if (e.target.dataset.toggle === "shippingAddressModal") {
        openModal('shippingAddressModal');
    }
});

// 윈도우 클릭시 모달 외부를 클릭하면 닫힘
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    // Get all modals
    var modals = document.getElementsByClassName('modal');

    // Check if the event target is not part of a modal
    for (var i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        }
    }
};
