// ************************************************
// ***************** Generate Message Function *******
function generateMessage(inputElement, message) {
  const errorMessage = `
  <div class="messageContainer absolute top-full  mt-1  flex justify-center bg-white text-red-600 text-xs font-medium px-2.5 py-1.5 md:py-2 rounded shadow z-10">
    <span contenteditable="true">${message}</span>
    <i class="fa-solid fa-circle-exclamation text-orange-500 text-sm mr-2"></i>
    <svg class="absolute bottom-full right-4 translate-y-1" width="15" height="10" viewBox="0 0 30 20" xmlns="http://www.w3.org/2000/svg">
      <polygon points="15, 0 30, 20 0, 20" fill="#ffffff" />
    </svg>
  </div>
`; // end error message

  inputElement.insertAdjacentHTML("afterend", errorMessage);

  // Scroll to the message container with spacing if not already visible
  const isVisible = isElementVisible(inputElement);

  if (!isVisible) {
    const scrollPosition =
      inputElement.getBoundingClientRect().top + window.pageYOffset - 100;
    window.scrollTo({ top: scrollPosition, behavior: "smooth" });
  }
  // Utility function to check element visibility
  function isElementVisible(inputElement) {
    const rect = inputElement.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <=
        (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }

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
// ****************************************
// ***** Fucntion to Check email *********
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
// ****************************************
// ***** Fucntion to count words *********
function countWords(element) {
  const text = element.value.trim();
  const words = text.split(/\s+/);
  return words.length;
}
// ****************************************
// ** Fucntion to check dangerous chars*****
function containsDangerousChars(element) {
  const text = element.value;
  const dangerousCharsRegex = /[<>&|#]/;
  return dangerousCharsRegex.test(text);
}
// ****************************************
// ** Fucntion to check only numbers*****
function containsOnlyNumbers(element) {
  const value = element.value.trim();
  const numberRegex = /^[0-9]+$/;
  return numberRegex.test(value);
}
// ****************************************
// ** function to check only number and dash *****
function containsOnlyNumbersAndDash(element) {
  const value = element.value.trim();
  const numberRegex = /^[0-9-]+$/;
  return numberRegex.test(value);
}

// ****************************************
// ** function to validate name *****
// only Persian letters and space
function validateName(element) {
  const value = element.value.trim();
  const persianLettersRegex = /^[\u0621-\u06CC\s]+$/;
  return persianLettersRegex.test(value);
}

// ****************************************
// ** function to validate password *****
// only English letters and numbers
function validatePassword(element) {
  const value = element.value.trim();
  const numberRegex = /\d/;
  const letterRegex = /[a-zA-Z]/;
  return numberRegex.test(value) && letterRegex.test(value);
}

// ****************************************
// ****Function to validate image type*****
function validateImageType(element) {
  const inputFile = element.files[0];
  const allowedTypes = ["image/jpeg", "image/png", "image/gif"];
  return allowedTypes.includes(inputFile.type);
}

// ****************************************
// ****Function to validate image size*****
function validateImageSize(element) {
  const inputFile = element.files[0];
  const maxSizeInBytes = 3 * 1024 * 1024; // 3MB
  return inputFile.size <= maxSizeInBytes;
}

// ****************************************
// ****Function to validate phone number*****
function validatePhoneNumber(element) {
  const phoneNumber = element.value.trim();
  const phoneNumberRegex = /^(07\d{8}|020\d{6})$/;
  return phoneNumberRegex.test(phoneNumber);
}

// ****************************************
// ****Function to validate future date *****
function isFutureDate(element) {
  // Convert the input date string to a Date object
  const enteredDate = new Date(element.value);
  // Get the current date
  const currentDate = new Date();
  currentDate.setDate(currentDate.getDate() + 1); // exclude today
  currentDate.setHours(0, 0, 0, 0); // Set current date to midnight

  // Compare the entered date with the current date
  if (enteredDate > currentDate) {
    return true; // entered date is a future date
  } else {
    return false; // entered date is today or in the past
  }
}
