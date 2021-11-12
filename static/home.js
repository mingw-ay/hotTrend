// 得到网站列表
const websitesList = document.querySelectorAll(".website");

websitesList.forEach((website) => {
  website.addEventListener("click", (e) => {
    const classes = Array.from(website.classList);
    //   判断是否有selected
    if (classes.indexOf("web_selected") == -1) {
      website.classList.add("web_selected");
      let i = document.createElement("i");
      i.classList.add("fas");
      i.classList.add("fa-check-circle");
      website.append(i);
    } else {
      website.classList.remove("web_selected");
      website.removeChild(website.lastChild);
    }
  });
});
