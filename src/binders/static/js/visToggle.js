function toggleVisibility() {
  var apiKeyInput = document.getElementById("user_key");
  var currentType = apiKeyInput.getAttribute("type");
  apiKeyInput.setAttribute("type", currentType === "password" ? "text" : "password");
  var visibilityImage = document.getElementById("visibilityImage");
  if (currentType === "password") {
// If the password is visible, set the image to invisible.png
    visibilityImage.src = "static/images/invisible.png";
    visibilityImage.alt = "hide key"
  } else {
// If the password is hidden, set the image to visibility.png
    visibilityImage.src = "static/images/visibility.png";
    visibilityImage.alt = "show key"
  }
}
