// ************************************************
// ***************** Generate Message Function *******
function generateMessage(inputElement, message) {
  const errorMessage = `
  <div class="messageContainer absolute top-full  mt-1  flex justify-center bg-white text-red-600 text-xs font-medium px-2.5 py-1.5 md:py-2 rounded shadow">
    <span contenteditable="true">${message}</span>
    <i class="fa-solid fa-circle-exclamation text-orange-500 text-sm mr-2"></i>
    <svg class="absolute bottom-full right-4 translate-y-1" width="15" height="10" viewBox="0 0 30 20" xmlns="http://www.w3.org/2000/svg">
      <polygon points="15, 0 30, 20 0, 20" fill="#ffffff" />
    </svg>
  </div>
`; // end error message

  inputElement.insertAdjacentHTML("afterend", errorMessage);
  // Disappear message automatically
  function disaapear() {
    document
      .querySelectorAll(".messageContainer")
      .forEach(function (container) {
        container.classList.add("hidden");
      });
  } // end disappear function
  setTimeout(disaapear, 5000);
} // end generate message function

// ************************************************
// ***** Fucntion to Check if  is Persian *********
function isPersianText(text) {
  const persianPattern =
    /^[\u0621-\u0628\u062A-\u063A\u0641-\u0642\u0644-\u0648\u0649\u067E\u0686\u0698\u06A9\u06AF\u06CC\s]+$/;
  return persianPattern.test(text);
}
