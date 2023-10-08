// Large humburgar menu
const container = document.getElementById("container");
const large_humgurgar = document.getElementById("large-humgurgar");
let sidebar_list_text = document.getElementsByClassName("sidebar-list-text");
const tazkira_column = document.getElementById("tazkira-column");
const img_div_large = document.getElementById("img-div-large"); // the photo div
const ul_large = document.getElementById("ul-large"); // Large ul

large_humgurgar.addEventListener("click", function () {
  if (container.classList.contains("grid-cols-[200px,1fr]")) {
    container.classList.remove("grid-cols-[200px,1fr]");
    container.classList.add("grid-cols-[70px,1fr]");
    // chamge table width
    if (tazkira_column != null) {
      tazkira_column.classList.remove("md:w-72");
      tazkira_column.classList.add("md:w-80");
    }
    // hide image
    img_div_large.classList.add("hidden");
    ul_large.classList.add("mt-12");
  } else if (container.classList.contains("grid-cols-[70px,1fr]")) {
    container.classList.remove("grid-cols-[70px,1fr]");
    container.classList.add("grid-cols-[200px,1fr]");
    // chamge table width
    if (tazkira_column != null) {
      tazkira_column.classList.remove("md:w-80");
      tazkira_column.classList.add("md:w-72");
    }
    // show image
    img_div_large.classList.remove("hidden");
    ul_large.classList.remove("mt-12");
  }
  // remove/add sidebar text
  for (let i = 0; i < sidebar_list_text.length; i++) {
    sidebar_list_text[i].classList.toggle("hidden");
  }
}); // end large-humburgar event listener

// *********************************************************
// ********* Mobile humburgar menu ***********************
const mobile_humburgar = document.getElementById("mobile-humburgar");
const mobile_nav = document.getElementById("mobile-nav");
const x_mark = document.getElementById("xmark");
mobile_humburgar.addEventListener("click", function () {
  mobile_nav.classList.remove("hidden");
  container.classList.add("opacity-40");
});
x_mark.addEventListener("click", function () {
  mobile_nav.classList.add("hidden");
  container.classList.remove("opacity-40");
});
