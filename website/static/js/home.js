function validatePassword() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmPassword").value;
    var passwordHelp = document.getElementById("passwordHelp");

    // Check if password meets criteria
    var isPasswordValid = true;

    // Minimum 8 characters
    if (password.length < 8) {
        passwordHelp.textContent = "Password must be at least 8 characters long";
        isPasswordValid = false;
    } else {
        passwordHelp.textContent = "";
    }

    // Additional criteria here
    var hasUppercase = /[A-Z]/.test(password);
    var hasLowercase = /[a-z]/.test(password);
    var hasDigit = /\d/.test(password);
    var hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (
        !hasUppercase ||
        !hasLowercase ||
        !hasDigit ||
        !hasSpecialChar
    ) {
        passwordHelp.textContent = "Password must contain at least one uppercase, one lowercase, one digit, and one special character";
        isPasswordValid = false;
    } else if (isPasswordValid) {
        passwordHelp.textContent = "";
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        passwordHelp.textContent = "Passwords do not match";
        isPasswordValid = false;
    }

    return isPasswordValid;
}


// toggle password visibility
function togglePasswordVisibility() {
    var passwordInput = document.getElementById("password");
    var confirmPasswordInput = document.getElementById("confirmPassword");
    var visibilityToggle = document.getElementById("visibilityToggle");

    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      confirmPasswordInput.type = "text";
      visibilityToggle.textContent = "Hide Password";
    } else {
      passwordInput.type = "password";
      confirmPasswordInput.type = "password";
      visibilityToggle.textContent = "Show Password";
    }
  }


const passwordToggleBtn = document.getElementById("password-toggle");
passwordToggleBtn.addEventListener("click", () => {
  const passwordInput = document.getElementById("password");
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    passwordToggleBtn.innerHTML = '<i class="bi bi-eye"></i>';
  } else {
    passwordInput.type = "password";
    passwordToggleBtn.innerHTML = '<i class="bi bi-eye-slash"></i>';
  }
});