// Toggle password visibility
document.getElementById('togglePassword').addEventListener('click', function () {
const passwordField = document.getElementById('id_password');
const icon = this.querySelector('i');

// Toggle password field type between 'password' and 'text'
const type = passwordField.type === 'password' ? 'text' : 'password';
passwordField.type = type;

// Toggle the icon between 'eye' and 'eye-slash'
if (type === 'password') {
    icon.classList.remove('fa-eye-slash');
    icon.classList.add('fa-eye');
} else {
    icon.classList.remove('fa-eye');
    icon.classList.add('fa-eye-slash');
}
});