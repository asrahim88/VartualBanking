// Function to toggle password visibility for password1
document.getElementById('togglePassword1').addEventListener('click', function () {
    const passwordField = document.getElementById('id_password1');
    const icon = this.querySelector('i');
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;

    // Toggle the icon between 'eye' and 'eye-slash'
    icon.classList.toggle('fa-eye');
    icon.classList.toggle('fa-eye-slash');
});

// Function to toggle password visibility for password2
document.getElementById('togglePassword2').addEventListener('click', function () {
    const passwordField = document.getElementById('id_password2');
    const icon = this.querySelector('i');
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;

    // Toggle the icon between 'eye' and 'eye-slash'
    icon.classList.toggle('fa-eye');
    icon.classList.toggle('fa-eye-slash');
});