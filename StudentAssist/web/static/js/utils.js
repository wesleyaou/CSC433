function setActiveTab(buttonId) {
    activeBtn = document.getElementById(buttonId);
    tabBtns = document.getElementsByClassName("tab-btn");

    for (i = 0; i < tabBtns.length; i++) {
        tabBtn[i].className = tabBtn[i].className.replace(" active-btn", "");
    }

    activeBtn.className += " active-btn";
}