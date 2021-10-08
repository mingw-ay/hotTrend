const { log } = console;

let pathname = document.location.pathname;

// do some judgement
if (pathname == "/") {
  // get the first category
  let li = document.querySelector(".list-group-item");
  li.firstElementChild.classList.add("selected");
} else {
  // get the specific node
  let link = document.querySelector(`.list-group-item a[href='${pathname}']`);
  link.classList.add("selected");
}
